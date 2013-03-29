# encoding: utf-8

"""
Copyright (c) 2012 Marian Steinbach

Hiermit wird unentgeltlich jeder Person, die eine Kopie der Software und
der zugehörigen Dokumentationen (die "Software") erhält, die Erlaubnis
erteilt, sie uneingeschränkt zu benutzen, inklusive und ohne Ausnahme, dem
Recht, sie zu verwenden, kopieren, ändern, fusionieren, verlegen
verbreiten, unterlizenzieren und/oder zu verkaufen, und Personen, die diese
Software erhalten, diese Rechte zu geben, unter den folgenden Bedingungen:

Der obige Urheberrechtsvermerk und dieser Erlaubnisvermerk sind in allen
Kopien oder Teilkopien der Software beizulegen.

Die Software wird ohne jede ausdrückliche oder implizierte Garantie
bereitgestellt, einschließlich der Garantie zur Benutzung für den
vorgesehenen oder einen bestimmten Zweck sowie jeglicher Rechtsverletzung,
jedoch nicht darauf beschränkt. In keinem Fall sind die Autoren oder
Copyrightinhaber für jeglichen Schaden oder sonstige Ansprüche haftbar zu
machen, ob infolge der Erfüllung eines Vertrages, eines Delikts oder anders
im Zusammenhang mit der Software oder sonstiger Verwendung der Software
entstanden.
"""

from pymongo import MongoClient
from pymongo import ASCENDING
from pymongo import DESCENDING
from bson.dbref import DBRef
import gridfs
import sys
import pprint
from hashlib import md5


class MongoDatabase(object):
    """
    Database handler for a MongoDB backend
    """

    def __init__(self, config, options):
        client = MongoClient(config.DB_HOST, config.DB_PORT)
        self.db = client[config.DB_NAME]
        self.config = config
        self.options = options
        self.fs = gridfs.GridFS(self.db)

    def setup(self):
        """
        Initialize database, if not yet done. Shouln't destroy anything.
        """
        self.db.sessions.ensure_index([('numeric_id', ASCENDING), ('ags', ASCENDING)], unique=True)
        self.db.attachments.ensure_index([('identifier', ASCENDING), ('ags', ASCENDING)], unique=True)
        self.db.submissions.ensure_index([('numeric_id', ASCENDING), ('ags', ASCENDING)], unique=True)
        self.db.fs.files.ensure_index(
            [
                ('ags', ASCENDING),
                ('filename', ASCENDING),
                ('uploadDate', DESCENDING),
            ],
            unique=True)

    def erase(self):
        """
        Delete all data from database.
        """
        self.db.sessions.remove({})
        self.db.attachments.remove({})
        self.db.submissions.remove({})
        self.db.fs.files.remove()
        self.db.fs.chunks.remove()

    def get_object(self, collection, key, value):
        """
        Return a document
        """
        result = self.db[collection].find_one({'ags': self.config.AGS, key: value})
        return result

    def get_object_id(self, collection, key, value):
        """
        Return the ObjectID of a document in the given collection identified
        by the given key:value pair
        """
        result = self.get_object(collection, key, value)
        if result is not None:
            if '_id' in result:
                return result['_id']

    def session_exists(self, id):
        if self.get_object_id('sessions', 'numeric_id', id) is not None:
            return True
        return False

    def attachment_exists(self, id):
        if self.get_object_id('attachments', 'identifier', id) is not None:
            return True
        return False

    def submission_exists(self, id):
        if self.get_object_id('submissions', 'numeric_id', id) is not None:
            return True
        return False

    def save_attachment(self, attachment):
        """
        Write attachment to DB and return ObjectID. If the attachment already exists,
        the existing attachment is updated in the database. If the attachment.content has
        changed, a new GridFS file version is added.
        """
        attachment_stored = self.get_object('attachments', 'identifier', attachment.identifier)
        attachment_fresh = attachment.dict()
        file_changed = False
        if attachment_stored is not None:
            # attachment exists in database and must be compared field by field
            print "Attachment %s is already in database with _id %s" % (attachment.identifier, str(attachment_stored['_id']))
            # check if file is referenced
            file_stored = None
            if 'file' in attachment_stored:
                # assuming DBRef in attachment.file
                assert type(attachment_stored['file']) == DBRef
                file_stored = self.db.fs.files.find_one({'_id': attachment_stored['file'].id})
            if file_stored is not None:
                # compare stored and submitted file
                if file_stored['length'] != len(attachment.content):
                    file_changed = True
                elif file_stored['md5'] != md5(attachment.content).hexdigest():
                    file_changed = True
        # Create new file version (if necessary)
        if file_changed or attachment_stored is None:
            file_oid = self.fs.put(attachment.content,
                filename=attachment.filename,
                ags=self.config.AGS)
            if self.options.verbose:
                sys.stdout.write("New file version stored with _id %s\n" % str(file_oid))
            attachment_fresh['file'] = DBRef(collection='fs.files', id=file_oid)

        # erase file content (since stored elsewhere above)
        attachment_fresh['content'] = None
        attachment_fresh['ags'] = self.config.AGS

        oid = None
        if attachment_stored is None:
            # insert new
            print "Inserting new attachment document"
            oid = self.db.attachments.insert(attachment_fresh)
        else:
            # Only do partial update
            oid = attachment_stored['_id']
            set_attributes = {}
            for key in attachment_fresh.keys():
                if key in ['last_modified']:
                    continue
                if key not in attachment_stored:
                    print "Key '%s' is not in stored attachment." % key
                    set_attributes[key] = attachment_fresh[key]
                elif attachment_stored[key] != attachment_fresh[key]:
                    print "Key '%s' value has changed." % key
                    set_attributes[key] = attachment_fresh[key]
                #else:
                #    print "Key '%s' is unchanged." % key
            if 'file' not in attachment_fresh:
                    set_attributes['file'] = attachment_stored['file']
            if file_changed or set_attributes != {}:
                set_attributes['last_modified'] = attachment_fresh['last_modified']
                self.db.attachments.update({'_id': oid},
                    {'$set': set_attributes})
        return oid

    def save_submission(self, submission, overwrite=False):
        """Write submission to DB and return ObjectID"""
        # TODO: Overwriting in case of changes would make more sense.
        submission_dict = submission.dict()
        # dereference submission-related attachments
        if 'attachments' in submission_dict:
            # replace attachment datasets with DBRef dicts
            for n in range(0, len(submission_dict['attachments'])):
                # Add attachment or return it's _id
                oid = self.save_attachment(submission_dict['attachments'][n])
                #print "Attachment _ID: ", oid
                submission_dict['attachments'][n] = DBRef(
                    collection='attachments', id=oid)
        #pprint.pprint(submission_dict)
        oid = self.get_object_id('submissions', 'numeric_id', submission.numeric_id)
        if (oid is None) or (overwrite == True):
            submission_dict['ags'] = self.config.AGS
            result = self.db.submissions.update(
                {'numeric_id': submission.numeric_id},
                submission_dict,
                upsert=True
            )
            if 'upserted' in result:
                oid = result['upserted']
        return oid

    def save_session(self, session):
        """
        Write session object to database. This means dereferencing all
        associated objects as DBrefs
        """
        session_dict = session.dict()
        # dereference session-related attachments
        if 'attachments' in session_dict:
            # replace attachment datasets with DBRef dicts
            for n in range(0, len(session_dict['attachments'])):
                # Add attachment or return it's _id
                oid = self.save_attachment(session_dict['attachments'][n])
                #print "Attachment _ID: ", oid
                session_dict['attachments'][n] = DBRef(
                    collection='attachments', id=oid)
            #pprint.pprint(session_dict['attachments'])
        # dereference agendaitem-related submissions
        if 'agendaitems' in session_dict:
            #pprint.pprint(session_dict['agendaitems'])
            # replace attachment datasets with DBRef dicts
            for agendaitem_id in session_dict['agendaitems'].keys():
                if 'submissions' not in session_dict['agendaitems'][agendaitem_id]:
                    continue
                for n in range(0, len(session_dict['agendaitems'][agendaitem_id]['submissions'])):
                    # Add submission or return it's _id
                    oid = self.save_submission(session_dict['agendaitems'][agendaitem_id]['submissions'][n])
                    #print "Submission _ID: ", oid
                    session_dict['agendaitems'][agendaitem_id]['submissions'][n] = DBRef(
                        collection='submissions', id=oid)
                #pprint.pprint(session_dict['agendaitems'])
        # TODO: dereference future references like committee
        session_dict['ags'] = self.config.AGS
        result = self.db.sessions.update(
            {'numeric_id': session.numeric_id},
            session_dict,
            upsert=True
        )
        if 'upserted' in result:
            return result['upserted']
        elif 'updatedExisting' in result:
            return self.get_object_id('sessions', 'numeric_id', session.numeric_id)
        else:
            sys.stderr.write("Error in MongoDatabase.save_session(): Database write result not in 'upserted' nor 'updatedExisting'\n")
            pprint.pprint(result)

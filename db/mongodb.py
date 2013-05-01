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
#import pprint
from hashlib import md5
import logging


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
        self.db.sessions.ensure_index([('numeric_id', ASCENDING), ('rs', ASCENDING)], unique=True)
        self.db.attachments.ensure_index([('identifier', ASCENDING), ('rs', ASCENDING)], unique=True)
        self.db.submissions.ensure_index([('numeric_id', ASCENDING), ('rs', ASCENDING)], unique=True)
        self.db.submissions.ensure_index('identifier', ASCENDING)
        self.db.fs.files.ensure_index(
            [
                ('rs', ASCENDING),
                ('filename', ASCENDING),
                ('uploadDate', DESCENDING),
            ],
            unique=True)

    def erase(self):
        """
        Delete all data from database.
        """
        self.db.queue.remove({'rs': self.config.RS})
        self.db.sessions.remove({'rs': self.config.RS})
        self.db.attachments.remove({'rs': self.config.RS})
        self.db.submissions.remove({'rs': self.config.RS})
        self.db.fs.files.remove({'rs': self.config.RS})
        self.db.fs.chunks.remove({'rs': self.config.RS})

    def get_object(self, collection, key, value):
        """
        Return a document
        """
        result = self.db[collection].find_one({'rs': self.config.RS, key: value})
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
        Write attachment to DB and return ObjectID.
        - If the attachment already exists, the existing attachment
          is updated in the database.
        - If the attachment.content has changed, a new GridFS file version
          is added.
        - If attachment is depublished, no new file is stored.
        """
        attachment_stored = self.get_object('attachments', 'identifier', attachment.identifier)
        attachment_fresh = attachment.dict()
        file_changed = False
        if attachment_stored is not None:
            # attachment exists in database and must be compared field by field
            logging.info("Attachment %s is already in db with _id=%s",
                attachment.identifier,
                str(attachment_stored['_id']))
            if self.options.verbose:
                sys.stdout.write("Attachment %s is already in database with _id %s\n" % (attachment.identifier, str(attachment_stored['_id'])))
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
        if ((file_changed and 'depublication' not in attachment_stored)
            or (attachment_stored is None)):
            file_oid = self.fs.put(attachment.content,
                filename=attachment.filename,
                rs=self.config.RS)
            logging.info("New file version stored with _id=%s", str(file_oid))
            if self.options.verbose:
                sys.stdout.write("New file version stored with _id %s\n" % str(file_oid))
            attachment_fresh['file'] = DBRef(collection='fs.files', id=file_oid)

        # erase file content (since stored elsewhere above)
        del attachment_fresh['content']
        attachment_fresh['rs'] = self.config.RS

        oid = None
        if attachment_stored is None:
            # insert new
            oid = self.db.attachments.insert(attachment_fresh)
            logging.info("Attachment %s inserted with _id %s",
                attachment.identifier, str(oid))
            if self.options.verbose:
                sys.stdout.write("Attachment %s inserted with _id %s\n" % (attachment.identifier, str(oid)))
        else:
            # Only do partial update
            oid = attachment_stored['_id']
            set_attributes = {}
            for key in attachment_fresh.keys():
                if key in ['last_modified']:
                    continue
                if key not in attachment_stored:
                    #print "Key '%s' is not in stored attachment." % key
                    set_attributes[key] = attachment_fresh[key]
                elif attachment_stored[key] != attachment_fresh[key]:
                    #print "Key '%s' value has changed." % key
                    set_attributes[key] = attachment_fresh[key]
                #else:
                #    print "Key '%s' is unchanged." % key

            if 'file' not in attachment_fresh and 'file' in attachment_stored:
                    set_attributes['file'] = attachment_stored['file']
            if file_changed or set_attributes != {}:
                set_attributes['last_modified'] = attachment_fresh['last_modified']
                self.db.attachments.update({'_id': oid},
                    {'$set': set_attributes})
        return oid

    def save_submission(self, submission):
        """Write submission to DB and return ObjectID"""
        submission_stored = self.get_object('submissions', 'numeric_id', submission.numeric_id)
        submission_fresh = submission.dict()
        submission_fresh['rs'] = self.config.RS

        # dereference submission-related attachments
        if 'attachments' in submission_fresh:
            # replace attachment datasets with DBRef dicts
            for n in range(0, len(submission_fresh['attachments'])):
                # Add attachment or return it's _id
                oid = self.save_attachment(submission_fresh['attachments'][n])
                #print "Attachment _ID: ", oid
                submission_fresh['attachments'][n] = DBRef(
                    collection='attachments', id=oid)
            # TODO: look for attachments that were there previously.

        # dereference superordinate
        if 'superordinate' in submission_fresh:
            sup = self.get_object('submissions', 'numeric_id', submission_fresh['superordinate']['numeric_id'])
            if sup is not None:
                submission_fresh['superordinate'] = DBRef(collection='submissions', id=sup['_id'])

        if submission_stored is not None:
            # now compare old and new dict
            set_attributes = {}
            for key in submission_fresh.keys():
                if key in ['last_modified']:
                    continue
                if key not in submission_stored:
                    #print "Key '%s' is not in stored attachment." % key
                    set_attributes[key] = submission_fresh[key]
                elif submission_stored[key] != submission_fresh[key]:
                    #print "Key '%s' value has changed." % key
                    set_attributes[key] = submission_fresh[key]
            if set_attributes != {}:
                set_attributes['last_modified'] = submission_fresh['last_modified']
                self.db.submissions.update({'_id': submission_stored['_id']}, {'$set': set_attributes})
            logging.info("Submission %s updated", submission_stored['_id'])
            if self.options.verbose:
                print "Submission %s updated" % submission_stored['_id']
            return submission_stored['_id']
        else:
            oid = self.db.submissions.insert(submission_fresh)
            logging.info("Submission %s inserted as new", oid)
            if self.options.verbose:
                print "Submission %s inserted as new" % oid
            return oid

    def save_session(self, session):
        """
        Write session object to database. This means dereferencing all
        associated objects as DBrefs
        """
        session_stored = self.get_object('sessions', 'numeric_id', session.numeric_id)
        session_dict = session.dict()
        session_dict['rs'] = self.config.RS
        # dereference session-related attachments
        if 'attachments' in session_dict:
            # replace attachment datasets with DBRef dicts
            for n in range(0, len(session_dict['attachments'])):
                # Add attachment or return it's _id
                oid = self.save_attachment(session_dict['attachments'][n])
                session_dict['attachments'][n] = DBRef(
                    collection='attachments', id=oid)
        # dereference agendaitem-related submissions
        if 'agendaitems' in session_dict:
            # replace attachment datasets with DBRef dicts
            for m in range(len(session_dict['agendaitems'])):
                if 'submissions' not in session_dict['agendaitems'][m]:
                    continue
                for n in range(0, len(session_dict['agendaitems'][m]['submissions'])):
                    # Add submission or return it's _id
                    oid = self.save_submission(session_dict['agendaitems'][m]['submissions'][n])
                    #print "Submission _ID: ", oid
                    session_dict['agendaitems'][m]['submissions'][n] = DBRef(
                        collection='submissions', id=oid)
        # TODO: dereference additional references like committee
        if session_stored is None:
            # insert new document
            oid = self.db.sessions.insert(session_dict)
            logging.info("Session %s inserted as new", oid)
            if self.options.verbose:
                sys.stdout.write("Session %s inserted as new\n" % (oid))
            return oid
        else:
            # compare old and new dict and then send update
            logging.info("Session %d updated with _id %s",
                session.numeric_id, session_stored['_id'])
            if self.options.verbose:
                sys.stdout.write("Session %d updated with _id %s\n" % (session.numeric_id, session_stored['_id']))
            set_attributes = {}
            for key in session_dict.keys():
                if key in ['last_modified']:
                    continue
                if key not in session_stored:
                    logging.debug("Key '%s' will be added to session", key)
                    if self.options.verbose:
                        sys.stdout.write("Key '%s' will be added to session\n" % key)
                    set_attributes[key] = session_dict[key]
                elif session_stored[key] != session_dict[key]:
                    logging.debug("Key '%s' will be updated", key)
                    if self.options.verbose:
                        sys.stdout.write("Key '%s' in session has changed\n" % key)
                    set_attributes[key] = session_dict[key]
            if set_attributes != {}:
                set_attributes['last_modified'] = session_dict['last_modified']
                self.db.sessions.update({'_id': session_stored['_id']}, {'$set': set_attributes})
            return session_stored['_id']

    def queue_status(self):
        """
        Prints out information on the queue
        """
        aggregate = self.db.queue.aggregate([
            {
                "$group": {
                    "_id": {
                        "rs": "$rs",
                        "status": "$status",
                        "qname": "$qname"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id.rs": 1}
            }])
        rs = None
        for entry in aggregate['result']:
            if entry['_id']['rs'] != rs:
                rs = entry['_id']['rs']
                print "RS: %s" % rs
            print "Queue %s, status %s: %d jobs" % (
                entry['_id']['qname'], entry['_id']['status'], entry['count'])

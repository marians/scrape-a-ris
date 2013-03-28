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
from bson.dbref import DBRef
import sys
import pprint


class MongoDatabase(object):
    """
    Database handler for a MongoDB backend
    """
    db = None
    config = None
    options = None

    def __init__(self, config, options):
        client = MongoClient(config.DB_HOST, config.DB_PORT)
        self.db = client[config.DB_NAME]
        self.config = config
        self.options = options

    def setup(self):
        """
        Initialize database, if not yet done. Shouln't destroy anything.
        """
        self.db.sessions.ensure_index([('numeric_id', ASCENDING), ('ags', ASCENDING)], unique=True)
        self.db.attachments.ensure_index([('identifier', ASCENDING), ('ags', ASCENDING)], unique=True)
        self.db.submissions.ensure_index([('numeric_id', ASCENDING), ('ags', ASCENDING)], unique=True)

    def erase(self):
        """
        Delete all data from database.
        """
        self.db.sessions.remove({})
        self.db.attachments.remove({})
        self.db.submissions.remove({})

    def get_object_id(self, collection, key, value):
        """
        Return the ObjectID of a document in the given collection identified
        by the given key:value pair
        """
        result = self.db[collection].find_one({key: value, 'ags': self.config.AGS})
        if result is not None:
            if '_id' in result:
                return result['_id']

    def session_exists(self, id):
        if self.get_object_id('sessions', 'numeric_id', id) is None:
            return False
        return True

    def attachment_exists(self, id):
        if self.get_object_id('attachments', 'identifier', id) is None:
            return False
        return True

    def submission_exists(self, id):
        if self.get_object_id('submissions', 'numeric_id', id) is None:
            return False
        return True

    def add_attachment(self, attachment, overwrite=False):
        """Write attachment to DB and return ObjectID"""
        # TODO: Overwriting in case of changes would make more sense.
        oid = self.get_object_id('attachments', 'identifier', attachment.identifier)
        if (oid is None) or (overwrite == True):
            attachment_dict = attachment.dict()
            attachment_dict['ags'] = self.config.AGS
            result = self.db.attachments.update(
                {'identifier': attachment.identifier},
                attachment_dict,
                upsert=True
            )
            if 'upserted' in result:
                oid = result['upserted']
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
                oid = self.add_attachment(submission_dict['attachments'][n],
                                          overwrite=self.options.update)
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
                oid = self.add_attachment(session_dict['attachments'][n],
                                          overwrite=self.options.update)
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
                    oid = self.save_submission(session_dict['agendaitems'][agendaitem_id]['submissions'][n],
                                              overwrite=self.options.update)
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

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

from document import Document
import hashlib


class Attachment(Document):
    """
    An attachment (Anhang) class
    """
    def __init__(self, identifier, name=None, mimetype=None, filename=None,
                 size=None, sha1=None, content=None, fulltext=None,
                 last_modified=None, thumbnails=None):
        self.identifier = identifier
        self.name = name
        self.mimetype = mimetype
        self.filename = filename
        self.size = size
        # SHA1 hash of the file's content
        self.sha1 = sha1
        # binary content of the file
        self.x_content = content
        # extracted text of the file
        self.fulltext = fulltext
        self.last_modified = last_modified
        self.thumbnails = thumbnails
        super(Attachment, self).__init__()

    @property
    def content(self):
        return self.x_content

    @content.setter
    def content(self, value):
        self.x_content = value
        if value is None:
            self.size = None
            self.sha1 = None
        else:
            self.size = len(value)
            self.sha1 = hashlib.sha1(value).hexdigest()

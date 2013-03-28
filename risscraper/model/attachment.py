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
import filters


class Attachment(Document):
    """
    An attachment (Anhang) class
    """
    def __init__(self, identifier, name=None, mimetype=None, filename=None,
                 size=None, sha1_checksum=None, content=None, path=None,
                 last_modified=None, thumbnails=None):
        self.identifier = identifier
        self.name = name
        self.mimetype = mimetype
        self.filename = filename
        self.size = size
        self.sha1_checksum = sha1_checksum
        self.content = content
        self.path = path
        self.last_modified = last_modified
        self.thumbnails = thumbnails
        super(Attachment, self).__init__()

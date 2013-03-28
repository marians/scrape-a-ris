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


class Submission(Document):
    """
    A submission (Vorlage) class
    """
    def __init__(self, numeric_id, identifier=None, title=None, subject=None, type=None,
                 date=None, original_url=None, attachments=None, superordinate=None):
        self.numeric_id = numeric_id
        self.identifier = identifier
        self.subject = subject
        self.x_title = title
        self.type = type
        self.x_date = date
        self.original_url = original_url
        self.attachments = attachments
        self.superordinate = superordinate
        super(Submission, self).__init__()

    @property
    def date(self):
        """Fancy getter for the date property"""
        return self.x_date

    @date.setter
    def date(self, value):
        """
        Fancy setter for the x_date property, which
        applies a string-to-datetime filter if ecessary
        """
        if type(value) == str:
            self.x_date = filters.datestring_to_datetime(value)
        else:
            self.x_date = value

    @property
    def title(self):
        return self.x_title

    @title.setter
    def title(self, value):
        self.x_title = value.strip()

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


class Session(Document):
    """
    A session (Sitzung) class
    """
    def __init__(self, numeric_id, identifier=None, committee_name=None,
                 committee_id=None, date_start=None, address=None,
                 description=None, attachments=None):
        #self._filters.append({
        #    'fieldname': 'date_start',
        #    'filter': lambda x: filters.datestring_to_datetime(x)
        #})
        self.numeric_id = numeric_id
        self.identifier = identifier
        self.committee_name = committee_name
        self.committee_id = committee_id
        self.x_date_start = date_start
        self.address = address
        self.description = description
        self.attachments = attachments
        super(Session, self).__init__()

    @property
    def date_start(self):
        """Fancy getter for the x_date_start property"""
        return self.x_date_start

    @date_start.setter
    def date_start(self, value):
        """
        Fancy setter for the x_date_start property, which
        applies a string-to-datetime filter if ecessary
        """
        if type(value) == str:
            self.x_date_start = filters.datestring_to_datetime(value)
        else:
            self.x_date_start = value

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

"""
This is a test suite for the "Document" class, which is the base class for all
objects to be stored in the database.
"""

from risscraper.model.document import Document
import datetime


def test_type():
    d = Document()
    assert type(d) == Document


def test_default_timestamp():
    d = Document()
    assert hasattr(d, 'last_modified')
    assert d.last_modified is not None
    assert getattr(d, 'last_modified') is not None
    assert type(d.last_modified) == type(datetime.datetime.utcnow())


def test_document_assignment():
    d = Document()
    d.foo = 1
    d.bar = 'two'
    assert d.foo == 1
    assert d.bar == 'two'



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

from risscraper.model.session import Session
import datetime
import sys


def test_basic_session():
    s = Session(1234)
    assert type(s) == Session
    del s


def test_default_timestamp():
    s = Session(1234)
    assert hasattr(s, 'last_modified')
    assert s.last_modified is not None
    assert type(s.last_modified) == type(datetime.datetime.utcnow())


def test_unnamed_args():
    s = Session(123456)
    assert hasattr(s, 'numeric_id')
    assert s.numeric_id == 123456


#def test_basic_session2():
#    s2 = model.Session()
#    s2.numeric_id = 1234
#    s2.identifier = "abc/1234"
#    s2.date_start = datetime.datetime(2013, 03, 01, 12, 0)
#    assert s2.validate() == True
#    del s2
#
#
#def test_session_constructor_assignment():
#    s = model.Session(numeric_id="1234",
#        identifier="abc / 1234",
#        date_start=datetime.datetime(2013, 3, 1, 12, 0))
#    assert s.numeric_id == 1234
#    assert s.identifier == "abc/1234"
#    assert s.date_start == datetime.datetime(2013, 3, 1, 12, 0)
#    assert s.validate() == True
#
#
#def test_date_conversion1():
#    s = model.Session()
#    s.date_start = "28.01.2013 17:00-18:15"
#    assert s.date_start == datetime.datetime(2013, 1, 28, 17, 0)
#
#
#def test_date_conversion2():
#    s = model.Session()
#    s.date_start = "28.01.2013 17:00"
#    assert s.date_start == datetime.datetime(2013, 1, 28, 17, 0)
#    del s
#
#
#def test_add_attachments():
#    s = model.Session()
#    s.attachments = []
#    s.attachments.append(model.Attachment(
#        identifier="foobar-ident"
#    ))
#    assert len(s.attachments) == 1
#    s.attachments.append(model.Attachment(
#        identifier="asddas-dfgdfg"
#    ))
#    assert len(s.attachments) == 2
#    assert type(s.attachments[0]) == type(model.Attachment())
#    assert type(s.attachments[0].dict()) == dict
#    sys.stdout.write("%s\n" % s.dict())

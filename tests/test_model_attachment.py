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

from risscraper.model.attachment import Attachment
import datetime
import sys


def test_basic_attachment():
    a = Attachment("foo")
    assert type(a) == Attachment


def test_default_timestamp():
    a = Attachment("blahblub1234")
    assert hasattr(a, 'last_modified')
    assert getattr(a, 'last_modified') is not None
    assert a.last_modified is not None
    assert type(a.last_modified) == type(datetime.datetime.utcnow())


def test_param_timestamp():
    lm = datetime.datetime(2012, 1, 1, 12, 0, 0)
    a = Attachment("blahblub1234", last_modified=lm)
    assert a.last_modified == lm


def test_unnamed_args():
    a = Attachment("blahblub1234")
    assert hasattr(a, "identifier")
    assert a.identifier == "blahblub1234"


def test_identifier_filter():
    a = Attachment("blahblub 1234")
    assert hasattr(a, "identifier")
    a.apply_filters()
    assert a.identifier == "blahblub1234"


def test_named_args():
    a = Attachment(identifier="foobar",
            name="Some Attachment",
            mimetype="application/pdf",
            filename="SomeAttachment.pdf",
            size=123456,
            sha1="439873428369057jsdfkjsh983239873523kj",
            content="\r\nThis is some messy content\r\n",
            thumbnails=[]
        )
    assert type(a) == Attachment
    assert a.size == 123456


def test_dict():
    a = Attachment("foobar")
    d = a.dict()
    assert type(d) == dict


def test_sha1():
    from hashlib import sha1
    a = Attachment("foobar")
    content = "Hello WOrld, this Is some Fabcy file content."
    a.content = content
    sha1 = sha1(content).hexdigest()
    assert sha1 == a.sha1

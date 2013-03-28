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

import argparse
from risscraper.scraper import Scraper
import datetime
import sys
import importlib


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scrape Dein Ratsinformationssystem')
    parser.add_argument('--config', '-c', dest='configname', default='config',
            help=("Name of the configuration module to use (e.g. 'config_koeln' for file 'config_koeln.py'). " +
                "Default: 'config'"))
    parser.add_argument('--verbose', '-v', action='count', default=0, dest="verbose")
    parser.add_argument('--update', '-u', dest="update", action="store_true",
            default=False, help='Set this to make the scraper update existing records. Default = No')
    parser.add_argument('--queue', '-q', dest="workfromqueue", action="store_true",
            default=False, help=('Set this flag to activate "greedy" scraping. This means that ' +
                'links from sessions to submissions are followed. Default = No'))
    parser.add_argument('--fulltext', '-f', dest="fulltext", action="store_true",
            default=False, help=('Set this flag to activate fulltext extraction during scraping. ' +
                'This slows down the scraping process and can also be done using an ' +
                'external script. Default = No'))
    parser.add_argument('--start', dest="start_month",
            default=False, help=('Find sessions and related content starting in this month. ' +
                'Format: "YYYY-MM"'))
    parser.add_argument('--end', dest="end_month",
            default=False, help=('Find sessions and related content up to this month. ' +
                'Requires --start parameter to be set, too. Format: "YYYY-MM"'))
    parser.add_argument('--sessionid', dest="session_id",
            default=False, help='Scrape a specific session, identified by its numeric ID')
    parser.add_argument('--sessionurl', dest="session_url",
            default=False, help='Scrape a specific session, identified by its detail page URL')
    parser.add_argument('--submissionid', dest="submission_id",
            default=False, help='Scrape a specific submission, identified by its numeric ID')
    parser.add_argument('--submissionurl', dest="submission_url",
            default=False, help='Scrape a specific submission, identified by its detail page URL')
    parser.add_argument('--erase', dest="erase_db", action="store_true",
            default=False, help='Erase all database content before start. Caution!')
    options = parser.parse_args()

    if options.configname:
        #config = __import__(options.configname, fromlist=[''])
        config = importlib.import_module(options.configname)

    db = None
    if config.DB_TYPE == 'mongodb':
        import db.mongodb
        db = db.mongodb.MongoDatabase(config, options)
        db.setup()
    #elif config.DB_TYPE == 'mysqldb':
    #    import db.mysqldb
    #    db = db.mysqldb.MysqlDatabase(config)
    #    db.setup()

    if options.erase_db:
        print "Erasing database"
        db.erase()

    scraper = Scraper(config, db, options)

    if options.session_id:
        scraper.get_session(session_id=int(options.session_id))

    if options.session_url:
        scraper.get_session(session_url=options.session_url)

    if options.submission_id:
        scraper.get_submission(submission_id=int(options.submission_id))

    if options.submission_url:
        scraper.get_submission(submission_url=options.submission_url)

    if options.start_month:
        try:
            options.start_month = datetime.datetime.strptime(options.start_month, '%Y-%m')
        except ValueError:
            sys.stderr.write("Bad format or invalid month for --start parameter. Use 'YYYY-MM'.\n")
            sys.exit()
        if options.end_month:
            try:
                options.end_month = datetime.datetime.strptime(options.end_month, '%Y-%m')
            except ValueError:
                sys.stderr.write("Bad format or invalid month for --end parameter. Use 'YYYY-MM'.\n")
                sys.exit()
            if options.end_month < options.start_month:
                sys.stderr.write("Error with --start and --end parameter: end month should be after start month.\n")
                sys.exit()
        else:
            options.end_month = options.start_month
        scraper.find_sessions(start_date=options.start_month, end_date=options.end_month)

    if options.workfromqueue:
        scraper.work_from_queue()

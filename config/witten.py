# encoding: utf-8

# AGS key (Amtlicher Gemeindeschlüssel) for the administrative unit.
#
# This is used as a namespace prefix in order to make identifiers
# in the system unique.
#
# Find the key for your German city/town/county here:
# https://www.destatis.de/gv/
#
# The AGS MUST have 8 digits. It MUST be a string, not a number,
# in order to save leading zeroes.
#
AGS = "05954036"

# Currently, only "mongodb" is supported
DB_TYPE = 'mongodb'

# Name of the MongoDB database
DB_NAME = 'scrapearis'

# Use "localhost" if MongoDB is running on the same machine
DB_HOST = 'localhost'

# MongoDB default port is 27017
DB_PORT = 27017

# Not used for MongoDB
DB_USER = ''
DB_PASS = ''

# SessionNet base url, should include trailing slash
BASE_URL = 'http://service.stadt-witten.de/session/bis/'

# Name to identify your crawler to the server
USER_AGENT_NAME = 'offeneskoeln/2.0_dev'

# Folder where attachments will be stored
ATTACHMENT_FOLDER = 'cache/attachments/' + AGS

# This requires you to have the tika Jar in the specified location.
# This will start the Java Runtime environment with the Jar for
# every file that will be processed. If you want the faster version,
# comment this out and use the server version described below.
#
TIKA_COMMAND = 'java -jar bin/tika-app-1.3.jar -eutf8 -t'

# If you prefer fast content extraction, start Tika as a server
# before running the scraper. Use a command like this:
#
# > java -jar bin/tika-app-1.3.jar -s -eutf8 -t 55555
#
# Make sure to set the according port below:
#
TIKA_SERVER = 'localhost'
TIKA_PORT = 55555
# ^ (The server option is not implemented yet!)

##### Page URL masks

# Month calender page
CALENDAR_MONTH_URL_PARSE_PATTERN = 'si0040.php?__cjahr={year:d}&__cmonat={month:d}'
CALENDAR_MONTH_URL_PRINT_PATTERN = BASE_URL + 'si0040.php?__cjahr=%d&__cmonat=%d'

# Session detail page
SESSION_DETAIL_URL_PARSE_PATTERN = 'to0040.php?__ksinr={session_id:d}'
SESSION_DETAIL_URL_PRINT_PATTERN = BASE_URL + 'to0040.php?__ksinr=%d'

# Committee detail page
COMMITTEE_DETAIL_URL_PARSE_PATTERN = 'kp0040.php?__kgrnr={committee_id:d}'
COMMITTEE_DETAIL_URL_PRINT_PATTERN = BASE_URL + 'kp0040.php?__kgrnr=%d'

# Submission detail page
SUBMISSION_DETAIL_URL_PARSE_PATTERN = 'vo0050.php?__kvonr={submission_id:d}'
SUBMISSION_DETAIL_URL_PRINT_PATTERN = BASE_URL + 'vo0050.php?__kvonr=%d'

# Attachment file download target file name
#ATTACHMENT_DOWNLOAD_TARGET = 'getfile.asp'
ATTACHMENT_DOWNLOAD_TARGET = 'ydocstart.php'


##### XPATH strings to find elements within pages

# session title within the session details page
SESSION_DETAIL_TITLE_XPATH = '//h1'

# table fields with session identifier, comittee name and more details
SESSION_DETAIL_IDENTIFIER_TD_XPATH = '//*[@id="smctablevorgang"]/tbody//td'

# link to committe within the session details page
#SESSION_DETAIL_COMMITTEE_LINK_XPATH = '//li[@class="smcmenucontext_fct_gremium"]/a'
SESSION_DETAIL_COMMITTEE_LINK_XPATH = '//a[@class="smccontextmenulink"]'


# table rows containing agendaitems on session detail page
#SESSION_DETAIL_AGENDA_ROWS_XPATH = '//*[@id="smc_page_to0040_contenttable1"]/tbody/tr'
SESSION_DETAIL_AGENDA_ROWS_XPATH = '//*[@class="smccontenttable smc_page_to0040_contenttable"]/tbody/tr'

# link to submission in agenda item row on session detail page
SESSION_DETAIL_AGENDA_ROWS_SUBMISSION_LINK_XPATH = './/a'

# table with session-related attachment downloads on session detail page
SESSION_DETAIL_ATTACHMENTS_XPATH = '//*[@id="smccontent"]//table'
SESSION_DETAIL_ATTACHMENTS_CONTAINER_CLASSNAME = 'smcdocbox'

# Same as above, for the submission detail page (Vorlagen-Detailseite)
SUBMISSION_DETAIL_TITLE_XPATH = SESSION_DETAIL_TITLE_XPATH
SUBMISSION_DETAIL_IDENTIFIER_TD_XPATH = SESSION_DETAIL_IDENTIFIER_TD_XPATH
# "Beratungsfolge" table
SUBMISSION_DETAIL_AGENDA_ROWS_XPATH = '//*[@class="smccontenttable smc_page_vo0050_contenttable"]/tbody/tr'
SUBMISSION_DETAIL_ATTACHMENTS_XPATH = SESSION_DETAIL_ATTACHMENTS_XPATH
SUBMISSION_DETAIL_ATTACHMENTS_CONTAINER_CLASSNAME = SESSION_DETAIL_ATTACHMENTS_CONTAINER_CLASSNAME


###### Result normalization mapping

RESULT_STRINGS = {
    'zur Kenntnis genommen': 'KENNTNIS_GENOMMEN',
    'einstimmig beschlossen': 'BESCHLOSSEN_EINSTIMMIG',
    u'einstimmig mit \xc4nderung / teilweise beschlossen': 'BESCHLOSSEN_EINSTIMMIG_GEAENDERT',
    'mit Mehrheit beschlossen': 'BESCHLOSSEN_MEHRHEIT',
    'mehrheitlich beschlossen': 'BESCHLOSSEN_MEHRHEIT',
    u'mehrheitlich mit \xc4nderung /teilweise beschlossen': 'BESCHLOSSEN_MEHRHEIT_GEAENDERT',
    'in Form von WAHLEN beschlossen': 'BESCHLOSSEN_DURCH_WAHLEN',
    'einstimmig abgelehnt': 'ABGELEHNT_EINSTIMMIG',
    'mehrheitlich abgelehnt': 'ABGELEHNT_MEHRHEIT',
    'verwiesen in:': 'VERWIESEN',
    'in der Sitzung vertagt': 'VERTAGT_IN_SITZUNG',
    u'vor Eintritt in die Tagesordnung zur\xfcckgezogen': 'ZURUECKGEZOGEN',
    u'in der Sitzung zur\xfcckgezogen': 'ZURUECKGEZOGEN',
    'abgesetzt': 'ABGESETZT',
    'von der Tagesordnung abgesetzt': 'ABGESETZT',
    'Verwaltung wird so verfahren': 'AKZEPTIERT',
    'schriftlicher Bericht/Vorlage wurde zugesagt': 'BERICHT_ZUGESAGT',
    'wird in der Verwaltung weiterbearbeitet': 'WEITERBEARBEITUNG_IN_VERWALTUNG',
    'durch STELLUNGNAHME der Verwaltung erledigt': 'ERLEDIGT_STELLUNGNAHME_VERWALTUNG',
    u'durch andere Beschl\xfcsse erledigt': 'ERLEDIGT_DURCH_ANDERE_BESCHLUESSE',
    'ohne Empfehlung behandelt': 'BEHANDELT_OHNE_EMPFEHLUNG',
    'Siehe Bemerkungsfeld': 'SONSTIGES',
    'siehe Protokoll': 'SONSTIGES',
    'Quorum wurde erreicht': 'QUORUM_ERREICHT'
}

# Number of seconds to wait between requests. Increase this
# if the systems behaves unstable (seconds)
WAIT_TIME = 0.2

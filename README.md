# Scrape-A-RIS

## English summary

Scrape-A-RIS is a scraper for assembly information systems (Ratsinformationssysteme, RIS)
using Somacos SessionNet, written in Python. Scrape-a-RIS is the successor of 
[cologne-ris-scraper](https://github.com/marians/cologne-ris-scraper) and is usable
for SessionNet instances in numerous municipalities (in Germany, mainly).


## German information

Scrape-A-RIS ist ein Scraper für Ratsinformationssysteme (RIS), die das System SessionNet 
verwenden. Scrape-A-RIS ist der Nachfolger von [cologne-ris-scraper](https://github.com/marians/cologne-ris-scraper)
und kann für zahlreiche Kommunen eingesetzt werden.

Scrape-A-RIS kann verwendet werden, um die strukturierten Daten und Inhalte aus Sitzungen, Tagesordnungspunkten,
Beschlussvorlagen, Anträgen und Anhängen auszulesen und diese in einer Datenbank abzulegen. Das Wort [Scraper](http://de.wikipedia.org/wiki/Screen_Scraping)
deutet auf die Funktionsweise hin: die Inhalte werden so aus den HTML-Seiten des RIS gelesen, wie sie für ganz
normale Besucher im Web angezeigt werden.

### Systemanforderungen

Scrape-A-RIS ist in Python geschrieben und wurde bislang mit Python-Version 2.7.2 auf Mac OS X getestet.

Daten werden in einer [MongoDB](http://www.mongodb.org/) Datenbank gespeichert. Bisher wurde Version 2.2 getestet.

TODO: Weitere requirements (Pyhton-Module, Kommandozeilentools) beschreiben

### Installation

Synopsis:

1. Mit virtualenv eine Python-Umgebung einrichten und diese starten
2. Die folgenden Python-Mdule installieren

    lxml==3.1.0
    mechanize==0.2.5
    parse==1.6.1
    py==1.4.13
    pymongo==2.4.2
    pytest==2.3.4
    python-magic==0.4.3
    wsgiref==0.1.2

3. MongoDB starten
4. Konfigurationsdatei config_example.py kopieren zu config.py, config.py anpassen
5. Optional (für Volltext-Extraktion aus PDFs etc.): Apache Tika herunter laden und Pfad in der Konfigurationsdatei eintragen

TODO: Ausführliche Beschreibung der erstmaligen Einrichtung

### Konfiguration

Die Konfiguration wird in config_example.py erläutert.

### Anwendung

Alle Kommandozeilen-Parameter werden erläutert, wenn das Hauptscript wie folgt aufgerufen wird:

    >>> python main.py --help

Mit diesem Aufruf können Inhalte für Februar und März 2013 abgerufen werden:

    >>> python main.py --start="2013-02" --end="2013-03" -q -v -u

So werden dabei direkt die Volltexte aus Dokumenten-Anhängen erfasst:

    >>> python main.py --start="2013-02" --end="2013-03" -f -q -v -u

TODO: Ausführliche Beschreibung

## Feedback

Bitte nutze den [Issues](https://github.com/marians/scrape-a-ris/issues) Bereich in diesem Github repository, um
Bugs zu melden.

## Unterstützung

Die Entwicklung an Scrape-a-RIS leiste ich unentgeldlich, dafür verzichte ich auf das Einkommen, das mit der Bearbeitung
von Aufträgen verbunden ist. Wenn Dir Scrape-a-RIS einen Dienst erweist und Du die Entwicklung unterstützen möchtest,
freue ich mich über eine Spende.

Spenden via [Gittip](https://www.gittip.com/marians/) | [PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=NJF88AWULCKCQ)

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

#import socket
#import time
import sys
import subprocess


#def extract(data, host="127.0.0.1", port=55555):
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    sock.connect((host, port))
#    response = ''
#    sock.sendall(data)
#    sock.shutdown(socket.SHUT_WR)
#    while 1:
#        chunk = sock.recv(1024)
#        if data == "":
#            break
#        response += chunk
#        time.sleep(0.01)
#    sock.close()
#    return response


def extract_from_file(path, tika_cmd):
    #sys.stdout.write(config.TIKA_COMMAND)
    cmd = tika_cmd + ' ' + path
    output, error = subprocess.Popen(
            cmd.split(' '), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate()
    if error.strip() != '':
        sys.stderr.write("Error calling tika (util.tikaclient.extract): %s\n" % error)
    return output.strip()

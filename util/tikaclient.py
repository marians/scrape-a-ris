# encoding: utf-8

#import socket
#import time
import sys
import config
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


def extract_from_file(path):
    #sys.stdout.write(config.TIKA_COMMAND)
    cmd = config.TIKA_COMMAND + ' ' + path
    output, error = subprocess.Popen(
            cmd.split(' '), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate()
    if error.strip() != '':
        sys.stderr.write("Error calling tika (util.tikaclient.extract): %s\n" % error)
    return output.strip()

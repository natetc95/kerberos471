######################################################
#
# Kerberos Authentication Server Service
# Nate Christianson
# ECE 471
# University of Arizona
#
######################################################

import socket
import sys

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('127.0.0.1', 88))
ss.listen(5)
cs, addr = ss.accept()
while cs:
    msg = cs.recv(1024)
    if msg:
        msg = msg.split('\0')
        for m in msg:
            if m == '':
                pass
            elif m == 'KERBEROS_ESTABLISH_CONN':
                print 'CONN: Client at ' + addr[0] + ':' + str(addr[1]) + ' is establishing a connection!'
                print 'KERBEROS: :)'
                cs.send(':)')
            elif m == 'KERBEROS_INIT':
                print 'CONN: Authentication request received from ' + addr[0] + ':' + str(addr[1]) + '!'
            elif m == 'KERBEROS_ABORT':
                print 'CONN: Client advised abort!'
                sys.exit(-1)
            else:
                print m
    elif not msg:
        break
cs.close()

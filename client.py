######################################################
#
# Kerberos Authentication Client Service
# Nate Christianson
# ECE 471
# University of Arizona
#
######################################################

import socket
import time

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('127.0.0.1', 88))
print 'CLIENT: Establishing connection to KERBEROS!'
cs.send('KERBEROS_ESTABLISH_CONN\0')
print 'CLIENT: Awaiting response'
while True:
    msg = cs.recv(1024)
    if msg:
        print 'KERBEROS: ' + msg
        break
    else:
        break
print 'CLIENT: Initializing request for KERBEROS authentication!'
cs.send('KERBEROS_INIT\0')
cs.shutdown(0)
cs.close()

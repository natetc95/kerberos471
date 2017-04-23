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
import json

print """  _  __         _                        _  _ _____ _ 
 | |/ /___ _ __| |__   ___ _ __ ___  ___| || |___  / |
 | ' // _ \ '__| '_ \ / _ \ '__/ _ \/ __| || |_ / /| |
 | . \  __/ |  | |_) |  __/ | | (_) \__ \__   _/ / | |
 |_|\_\___|_|  |_.__/ \___|_|  \___/|___/  |_|/_/  |_|
                                                      """
print " A Python Implementation of the Kerberos Authentication Protocol"
print " Authentication / Ticketing Server"
print " Python Version: " + sys.version
print """
 Nathaniel Christianson
 University of Arizona
 ECE 471

 Log:\n"""

def awaitResponse(cs, size=1024):
    while True:
        msg = cs.recv(size)
        if msg:
            print '  CONN: ' + msg
            return msg

def generateTGT():
    pass

def generateSK_TGS():
    from pycrypto.Hash import SHA as hAlgorithm
    import os
    key = hAlgorithm.new(os.urandom(8)).digest()[:8]
    return key

print generateSK_TGS()
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
            elif m == 'AM_I_ALONE':
                print '  CONN: Client asked if we were alive.\n  KERBEROS: Yes'
            elif m == 'SEND_AS_REQ_ACK':
                print '  CONN: Client wants to send AS_REQ.\n  KERBEROS: KERBEROS_SEND_TRAFFIC'
                cs.send('KERBEROS_SEND_TRAFFIC')
                awaitResponse(cs)
                print '  KERBEROS: KERBEROS_TRAFFIC_RECV'
                cs.send('KERBEROS_TRAFFIC_RECV')
            elif m == 'KERBEROS_ESTABLISH_CONN':
                print '  CONN: Client at ' + addr[0] + ':' + str(addr[1]) + ' is establishing a connection!'
                print '  KERBEROS: CLIENT_CONN_ESTABLISHED'
                cs.send('CLIENT_CONN_ESTABLISHED')
            elif m == 'KERBEROS_AUTH_INIT':
                print '  CONN: Authentication request received from ' + addr[0] + ':' + str(addr[1]) + '!'
                print '  KERBEROS: CLIENT_SEND_AS_REQ'
                cs.send('CLIENT_SEND_AS_REQ')
                while True:
                    msg = cs.recv(2048)
                    if msg:
                        try:
                            print '  ' + msg
                            print '  ' + json.loads(msg)["un"]
                        except Exception as e:
                            print e
                        break
                    else: break
            elif m == 'KERBEROS_ABORT':
                print '  CONN: Client advised abort!'
                sys.exit(-1)
            else:
                print '  CONN: ' + m
    elif not msg:
        break
cs.close()
print "  CONN: Connection Closed!"
while True:
    pass

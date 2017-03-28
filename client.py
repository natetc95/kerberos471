######################################################
#
# Kerberos Authentication Client Service
# Nate Christianson
# ECE 471
# University of Arizona
#
######################################################

import socket
import sys
import time
import getpass

class KerberosClient(object):

    def __init__(self, host='localhost', port=88, verbose=True):
        self.HOST = host
        self.PORT = port
        self.verbose = verbose
        self.connected = False
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cs.setblocking(0)
        self.cs.settimeout(5)
        if verbose:
            print """  _  __         _                        _  _ _____ _ 
 | |/ /___ _ __| |__   ___ _ __ ___  ___| || |___  / |
 | ' // _ \ '__| '_ \ / _ \ '__/ _ \/ __| || |_ / /| |
 | . \  __/ |  | |_) |  __/ | | (_) \__ \__   _/ / | |
 |_|\_\___|_|  |_.__/ \___|_|  \___/|___/  |_|/_/  |_|
                                                      """
            print " A Python Implementation of the Kerberos Authentication Protocol"
            print " Client Application"
            print " Python Version: " + sys.version
            print "\n Nathaniel Christianson\n University of Arizona\n ECE 471\n\n Log:\n"
        time.sleep(1)

    def isConnected(self, verbose = False):
        conn_stat = True
        self.cs.settimeout(0.1)
        if verbose:
            print "  CLIENT: Am I alone?"
        try:
            self.cs.send("AM_I_ALONE")
        except:
            conn_stat = False
        self.cs.settimeout(5)
        if verbose:
            if conn_stat:
                print "  KERBEROS: You are not alone."
            else:
                print "  ERROR: No response."
        return self.connected and conn_stat

    def awaitResponse(self, size=1024):
        try:
            while True:
                msg = self.cs.recv(size)
                if msg:
                    print '  KERBEROS: ' + msg
                    return msg
        except:
            pass
        print '  ERROR: Server did not respond in time.'
        return 'timeout'

    def establishConnection(self):
        if not self.isConnected():
            try:
                self.cs.connect((self.HOST, self.PORT))
                print '  CLIENT: Establishing connection to KERBEROS at '+ self.HOST + ':' + str(self.PORT) + '!'                
                self.connected = True
            except:
                print "  ERROR: Failed to connect to KERBEROS server!"
                return -1
        self.cs.send('KERBEROS_ESTABLISH_CONN\0')
        print '  CLIENT: Awaiting response'
        try:
            while True:
                msg = self.cs.recv(1024)
                if msg:
                    print '  KERBEROS: ' + msg
                    break
                else:
                    break
        except:
            print '  ERROR: No response from KERBEROS'
            return -1
        return 1

    def initializeKerberos(self):
        if self.isConnected():
            try:
                self.cs.send('KERBEROS_AUTH_INIT\0');
                print '  CLIENT: Authentication request sent to KERBEROS!'
            except:
                print '  ERROR: Failed to send request'
                return -1
            try:
                while True:
                    msg = self.cs.recv(1024)
                    if msg:
                        print '  KERBEROS: ' + msg
                        if msg == 'CLIENT_SEND_AS_REQ':
                            uname = raw_input('  > Principal Client: ')
                            sname = raw_input('  > Principal Service: ')
                            ltime = raw_input('  > Lifetime (minutes): ')
                            pword = getpass.getpass('  > Password: ')
                            self.cs.send('{"un": "' + uname + '", "sn": "' + sname + '", "lt": ' + ltime + '}')
                        break
                    else:
                        break
            except:
                print '  ERROR: No response from KERBEROS'
                return -1
            return 1

    def send_AS_REQ(self, principalClient, principalService, lifetime):
        if self.isConnected():
            print '  CLIENT: Sending AS request. Awaiting Server confirmation...'
            self.cs.send("SEND_AS_REQ_ACK")
            if self.awaitResponse() == 'KERBEROS_SEND_TRAFFIC':
                print "ayy"
                self.cs.send('{"pC": "%s", "pS": "%s", "lt": %s}' % (principalClient, principalService, str(lifetime)))

    def closeConnection(self):
        if self.isConnected():
            self.cs.shutdown(0)
            self.cs.close()
            print '  CLIENT: Connection Closed!'
            return 1
        else:
            print '  ERROR: You are not connected to anything!'
            return -1
    
if __name__ == '__main__':
    client = KerberosClient()
    client.establishConnection()
    client.send_AS_REQ("nate", "nate", 11)
    client.closeConnection()
    while True: pass

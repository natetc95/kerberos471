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

    def __init__(self, host='localhost', port=88):
        self.HOST = host
        self.PORT = port
        self.connected = False
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cs.setblocking(0)
        self.cs.settimeout(5)

    def isConnected(self):
        return self.connected

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

    print """  _  __         _                        _  _ _____ _ 
 | |/ /___ _ __| |__   ___ _ __ ___  ___| || |___  / |
 | ' // _ \ '__| '_ \ / _ \ '__/ _ \/ __| || |_ / /| |
 | . \  __/ |  | |_) |  __/ | | (_) \__ \__   _/ / | |
 |_|\_\___|_|  |_.__/ \___|_|  \___/|___/  |_|/_/  |_|
                                                      """
    print " A Python Implementation of the Kerberos Authentication Protocol"
    print " Client Application"
    print " Python Version: " + sys.version
    print """
 Nathaniel Christianson
 University of Arizona
 ECE 471

 Log:\n"""
    time.sleep(1)
    client = KerberosClient()
    client.establishConnection()
    client.initializeKerberos()
    client.closeConnection()
    while True: pass

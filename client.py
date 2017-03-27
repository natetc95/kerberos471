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
                self.connected = True
            except:
                print "ERROR: Failed to connect to KERBEROS server!"
                return -1
        print 'CLIENT: Establishing connection to KERBEROS!'
        self.cs.send('KERBEROS_ESTABLISH_CONN\0')
        print 'CLIENT: Awaiting response'
        try:
            while True:
                msg = self.cs.recv(1024)
                if msg:
                    print 'KERBEROS: ' + msg
                    break
                else:
                    break
        except:
            print 'ERROR: No response from KERBEROS'
            return -1
        return 1

    def initializeKerberos(self):
        if self.isConnected():
            try:
                print 'CLIENT: Initializing request for KERBEROS authentication!'
                self.cs.send('KERBEROS_INIT\0');
            except:
                print 'ERROR: Failed to initialize request'
                return -1
            try:
                while True:
                    msg = self.cs.recv(1024)
                    if msg:
                        print 'KERBEROS: ' + msg
                        if msg == 'CLIENT_SEND_CREDS':
                            uname = raw_input('  Username: ')
                            pword = getpass.getpass('  Password: ')
                        break
                    else:
                        break
            except:
                print 'ERROR: No response from KERBEROS'
                return -1
            return 1

    def closeConnection(self):
        if self.isConnected():
            self.cs.shutdown(0)
            self.cs.close()
            print 'CLIENT: Connection Closed!'
            return 1
        else:
            print 'ERROR: You are not connected to anything!'
            return -1
    
if __name__ == '__main__':
    client = KerberosClient()
    client.establishConnection()
    client.initializeKerberos()
    client.closeConnection()

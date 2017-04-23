######################################################
#
# Chat Client for use with Kerberos Authenication Protocol
# Nate Christianson
# ECE 471
# University of Arizona
#
######################################################

from Tkinter import *
from tkSimpleDialog import *
import tkMessageBox
from ScrolledText import *
import json, threading, time, socket, select
import base64
from Crypto import Random
from Crypto.Cipher import AES

class Client2:
    # Kerberos Client
    # Handles all encryption to and from
    def __init__(self, app):
        self.app = app
        self.type = 'kerberos'
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.cs.connect(('localhost', 32667))
        except socket.error as serr:
            self.app.say('SERVER', 'An error occurred while connecting!', 'C')
        self.key = 'F481544571902EEE0A85E2FA4B855CF8';
        self.cipher = AES.new( self.key, AES.MODE_ECB)
        self.pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        self.unpad = lambda s : s[0:-ord(s[-1])]
        self.t = threading.Thread(target=self.startThread)
        self.t.daemon = True
         
    def startThread(self):
        inputs = [self.cs]
        while 1:
            data = self.cs.recv(1024)
            if data:
                self.app.recieve(data)
    
    def encrypt(self, string):
        padded_string = self.pad(string)
        encrypted = base64.b64encode(self.cipher.encrypt( padded_string ))
        return encrypted

    def decrypt(self, encrypted):
        decoded = base64.b64decode(encrypted)
        return self.unpad(self.cipher.decrypt(enc))

    def start(self):
        data = dict()
        if self.app.username is None:
            data['type'] = 'hello'
            self.cs.send(self.encrypt(json.dumps(data)))
            while 1:
                data = self.cs.recv(1024)
                if data:
                    self.app.username = 'anon' + str(data)
                    break
            data = dict()
            data['type'] = 'login'
            data['name'] = self.app.username
            self.cs.send(self.encrypt(json.dumps(data)))
        else:
            data['type'] = 'login'
            data['name'] = self.app.username
            self.cs.send(self.encrypt(json.dumps(data)))
        self.t.start()

    def sendmsg(self, msg, typs='msg'):
        data = dict();
        data['type'] = typs
        data['name'] = self.app.username
        data['msg'] = msg
        self.cs.send(self.encrypt(json.dumps(data)))

    def shutdown(self):
        self.sendmsg('', 'shutdown')
        self.cs.shutdown(0)
        self.cs.close()
class Client:
    # Unencrypted Client
    # There is no encryption
    def __init__(self, app):
        self.type = 'non-kerb'
        self.app = app
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.cs.connect(('localhost', 32667))
        except socket.error as serr:
            self.app.say('SERVER', 'An error occurred while connecting!', 'C')
        self.t = threading.Thread(target=self.startThread)
        self.t.daemon = True
         
    def startThread(self):
        inputs = [self.cs]
        while 1:
            data = self.cs.recv(4096)
            if data:
                self.app.recieve(data)
    
    def start(self):
        data = dict()
        if self.app.username is None:
            data['type'] = 'hello'
            self.cs.send(json.dumps(data))
            while 1:
                data = self.cs.recv(1024)
                if data:
                    self.app.username = 'anon' + str(data)
                    break
            data = dict()
            data['type'] = 'login'
            data['name'] = self.app.username
            self.cs.send(json.dumps(data))
        else:
            data['type'] = 'login'
            data['name'] = self.app.username
            self.cs.send(json.dumps(data))
        self.t.start()

    def sendmsg(self, msg, type='msg'):
        data = dict();
        data['type'] = type
        data['name'] = self.app.username
        data['msg'] = msg
        self.cs.send(json.dumps(data))

    def shutdown(self):
        self.sendmsg('', 'shutdown')
        self.cs.shutdown(0)
        self.cs.close()

class Application(Frame):
    def recieve(self, jsonstr):
        obj = json.loads(jsonstr)
        if obj['msg'] == 'Server is shutting down!':
            self.client.cs.close()
            self.client = None;
            self.say(obj['name'], obj['msg'], obj['que'])
        else:
            self.say(obj['name'], obj['msg'], obj['que'])

    def say(self, who, what, t='Y'):
        self.chatbox['state'] = "normal"
        str(what).replace('\n', '')
        str(who).replace('\n', '')
        self.chatbox.insert('end', "[" + t + "][" + str(who) + "]: " + str(what) + "\n")
        self.chatbox.see('end')
        self.chatbox['state'] = "disabled"
    
    def clearbox(self):
        self.chatbox['state'] = "normal"
        self.chatbox.delete(1.0, 'end')
        self.chatbox['state'] = "disabled"

    def send(self, args=None):
        if self.client != None:
            what = self.inputBox.get(1.0, END)
            what = ' '.join(what.split())
            if what != '':
                self.say(self.username, what)
                self.client.sendmsg(what)
                self.inputBox.delete(1.0, END)
        else:
            tkMessageBox.showwarning('No Server', 'You are not connected to the server!')

    def identify(self):
        if self.client is not None and self.client.type != 'kerberos':
            name = askstring("Get Identifier", "Name")
            if self.username is None:
                self.username = name
            else:
                q = self.username
                self.username = name
                self.client.sendmsg(q, 'namechange')
        else:
            tkMessageBox.showerror('Kerberos Encryption', 'You are securely connected via Kerberos.\nYou cannot change your identity!')

    def disconnect(self):
        if self.client is not None:
            self.client.shutdown()
            self.client = None
            self.say('CLIENT', 'Disconnecting from server...', 'C')

    def connectClient(self):
        self.say('CLIENT', 'Connecting to Server...', 'C')
        self.disconnect()
        if self.client is None:
            self.client = Client(self)
            self.client.start()
        else:
            tkMessageBox.showwarning('Already Connected', 'You are already connected to the server!')
    def kerberosClient(self):
        self.say('CLIENT', 'Connecting to encrypted Server...', 'C')
        self.disconnect()
        if self.client is None:
            self.client = Client2(self)
            self.client.start()
        else:
            tkMessageBox.showwarning('Already Connected', 'You are already connected to the server!')

    def shutdown(self):
        if self.client is None:
            self.root.destroy()
        else:
            self.client.shutdown()
            self.root.destroy()

    def createWidgets(self):

        self.chatbox = ScrolledText(self)
        self.chatbox['width'] = 50
        self.chatbox['height'] = 24
        self.chatbox['padx'] = 5
        self.chatbox['pady'] = 5
        self.chatbox['relief'] = 'flat'
        self.chatbox['state'] = "disabled"
        self.chatbox['font'] = ("Comic Sans MS", 10, "") # Intentionally coded Comic Sans
        self.grid(row=0, column=1, padx=5, pady=5)
        self.chatbox.pack()

        self.separator = Frame(self)
        self.separator['height'] = 10
        self.separator.pack()

        self.sendFrame = Frame(self)

        self.inputBox = Text(self.sendFrame)
        self.inputBox['width'] = 47
        self.inputBox['height'] = 2
        self.inputBox['relief'] = 'flat'
        self.inputBox['font'] = ("Comic Sans MS", 10, "")
        self.inputBox.pack({"side": "left"})

        self.separatorV = Frame(self.sendFrame)
        self.separatorV['width'] = 10
        self.separatorV.pack({"side": "left"})

        self.sendButton = Button(self.sendFrame)
        self.sendButton["text"] = "Send",
        self.sendButton["command"] = self.send
        self.sendButton.pack({"side": "left"})

        self.sendFrame.pack()

    def createMenubar(self, master = None):
        self.menubar = Menu(master)

        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label='Identify', command=self.identify)
        self.file_menu.add_command(label='Clear Log', command=self.clearbox)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', command=self.quit)

        self.connect_menu = Menu(self.menubar, tearoff=0)
        self.connect_menu.add_command(label='Encrypted', command=self.kerberosClient)
        self.connect_menu.add_command(label='Unencrypted', command=self.connectClient)
        self.connect_menu.add_separator()
        self.connect_menu.add_command(label='Disconnect', command=self.disconnect)

        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Connect", menu=self.connect_menu)

        master.config(menu=self.menubar)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.createMenubar(master)
        self.root = master
        self.root.title('Chat Client')
        self.root.bind('<Return>', self.send)
        self.client = None
        self.username = None

try:
    root = Tk()
    app = Application(root)
    app.mainloop()
except:
    pass
    
try:
    app.shutdown()
except:
    pass
from Tkinter import *
from ScrolledText import *
import socket, select, sys, time, json, threading
import base64
from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class Server:
    def __init__(self, app):
        self.app = app
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', 32667))
        self.server.listen(10)
        self.inputs = [self.server]
        self.count = 1000
        self.t = threading.Thread(target=self.startThread)
        self.t.daemon = True
        self.t.start()
        self.pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        self.unpad = lambda s : s[0:-ord(s[-1])]

    def decrypt(self, key, encrypted):
        decoded = base64.b64decode(encrypted)
        cipher = AES.new(key, AES.MODE_ECB)
        return self.unpad(cipher.decrypt(decoded))

    def startThread(self):
        while 1:
            read, write, error = select.select(self.inputs, [], [])
            for s in read:
                if s == self.server:
                    cs, addr = self.server.accept()
                    self.inputs.append(cs)
                else:
                    data = s.recv(4096)
                    if data:
                        send = dict()
                        try:
                            data = json.loads(data)
                            que = 'U'
                        except ValueError:
                            print 'Encrypted Data!'
                            data = json.loads(self.decrypt('F481544571902EEE0A85E2FA4B855CF8', data))
                            que = 'V'
                        try:
                            if data['type'] == 'shutdown':
                                self.inputs.remove(s)
                                self.app.log('User "%s" has disconnected.' % (data['name']))
                                send['que'] = 'S'
                                send['name'] = 'SERVER'
                                send['msg'] = '%s has disconnected from the server' % (data['name'])
                                for i in self.inputs:
                                    if i != s and i != self.server:
                                        i.send(json.dumps(send))
                            elif data['type'] == 'hello':
                                s.send(str(self.count))
                                self.app.log('Assigned name "anon%s" to new user.' % (str(self.count)))
                                self.count += 1
                            elif data['type'] == 'login':
                                self.app.log('User logged in as "%s".' % (data['name']))
                                send['que'] = 'S'
                                send['name'] = 'SERVER'
                                send['msg'] = 'Welcome to the server. There are currently %i users online.' % (len(self.inputs) - 2)
                                s.send(json.dumps(send))
                                send = dict()
                                send['que'] = 'S'
                                send['name'] = 'SERVER'
                                send['msg'] = '%s has connected to the server' % (data['name'])
                                for i in self.inputs:
                                    if i != s and i != self.server:
                                        i.send(json.dumps(send))
                            elif data['type'] == 'namechange':
                                send['que'] = 'S'
                                send['name'] = 'SERVER'
                                send['msg'] = '%s changed their name to %s.' % (data['msg'], data['name'])
                                self.app.log('User "%s" has changed their name to "%s".' % (data['msg'], data['name']))
                                for i in self.inputs:
                                    if i != s and i != self.server:
                                        i.send(json.dumps(send))
                            else:
                                self.app.log('User "%s" sent a message: "%s".' % (data['name'], data['msg']))
                                send['que'] = que
                                send['name'] = data['name']
                                send['msg'] = data['msg']
                                for i in self.inputs:
                                    if i != s and i != self.server:
                                        i.send(json.dumps(send))
                        except TypeError:
                            print 'ERROR'
    def shutdown(self):
        for i in self.inputs:
            if i != self.server:
                i.send('{"que": "S", "name": "SERVER", "msg": "Server is shutting down!"}')


class Application(Frame):
    def say(self, who, what):
        self.chatbox['state'] = "normal"
        str(what).replace('\n', '')
        str(who).replace('\n', '')
        self.chatbox.insert('end', "[" + str(who) + "]: " + str(what) + "\n")
        self.chatbox.see('end')
        self.chatbox['state'] = "disabled"
    def log(self, what):
        self.chatbox['state'] = "normal"
        str(what).replace('\n', '')
        self.chatbox.insert('end', str(what) + "\n")
        self.chatbox.see('end')
        self.chatbox['state'] = "disabled"
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

        self.sendButton = Button(self)
        self.sendButton["text"] = "Quit",
        self.sendButton["command"] = self.quit
        self.sendButton.pack()

    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.root = master
        self.root.title('Chat Server')
        self.s = Server(self)

root = Tk()
app = Application(root)
app.mainloop()
app.s.shutdown()
root.destroy()
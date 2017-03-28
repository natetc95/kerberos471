import time
import os
import threading

def runPy(name):
    os.system("start cmd /c python " + name)

authServer = threading.Thread(target=runPy, args=("server.py",), name="auth_server")
client = threading.Thread(target=runPy, args=("client.py",), name="client")
authServer.start()
client.start()
 

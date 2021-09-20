import time
import socket
import threading
from datetime import datetime

class newClient:
    HEADER = 64
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "[DISCONNECT]"
    CHECK_CONNECTION_MESSAGE  = "[CHECK_CONNECTION]"
    CMD_MESSAGE = "[CMD]"
    TEXT_MESSAGE = "[TEXT]"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER = socket.gethostbyname(socket.gethostname())
    PORT = 55000
    ADDR = (SERVER, PORT)

    entryLog = []

    client.settimeout(0.25)

    clientIsConnected = False
    
    def start(self, __SERVER__ = socket.gethostbyname(socket.gethostname()), __PORT__ = 55000):
        self.PORT = __PORT__
        self.SERVER = __SERVER__

        ADDR = (self.SERVER, self.PORT)
        self.ADDR = ADDR
        
        try:
            self.log = open(f"log-client-{__SERVER__}:{__PORT__}.txt", 'a')
        except:
            self.log = open(f"log-client-{__SERVER__}:{__PORT__}.txt", 'r+')

        self.entryLog = self.log.readlines()
        self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARING...] Client starting on {self.SERVER}:{self.PORT}/n")
        self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARING...] Client starting on {self.SERVER}:{self.PORT}")
        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARING...] Client starting on {self.SERVER}:{self.PORT}")

    def connect(self):
        try:
            self.client.connect(self.ADDR)
            
            self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Connected to {self.SERVER}:{self.PORT}.../n")
            self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Connected to {self.SERVER}:{self.PORT}...")
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Connected to {self.SERVER}:{self.PORT}...")

            checkConnection = threading.Thread(target = self.__checkConnection__, args = (), daemon = True)
            self.clientIsConnected = True
            checkConnection.start()
        except:
            self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Can't connect to {self.SERVER}:{self.PORT}.../n")
            self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Can't connect to {self.SERVER}:{self.PORT}...")
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Can't connect to {self.SERVER}:{self.PORT}...")

    def disconnect(self):
        self.send(self.DISCONNECT_MESSAGE, msgKey=self.DISCONNECT_MESSAGE)
        self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {self.ADDR} Disconnected by client./n")
        self.entryLog(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {self.ADDR} Disconnected by client.")
        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {self.ADDR} Disconnected by client.")
    
    def close(self):
        self.client.close()
        self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]/n")
        self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]")
        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]")

    def send(self, msgValue, msgKey = "[TEXT]"):
        if self.clientIsConnected:
            msg = msgKey + " --> " + msgValue

            if msgValue != self.CHECK_CONNECTION_MESSAGE:
                self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] {msg}/n")
                self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] {msg}")
                print(f"[{datetime.now().strftime('''%H:%M:%S''')}] {msg}")
            message = msg.encode(self.FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(self.FORMAT)
            send_length += b' ' * (self.HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message)

            serverAnsw = "NONE"
            serverAnsw = self.client.recv(1024).decode(self.FORMAT)

            if serverAnsw != "NONE" and serverAnsw != self.CHECK_CONNECTION_MESSAGE:
                self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] {serverAnsw}/n")
                self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] {serverAnsw}")
                print(f"[{datetime.now().strftime('''%H:%M:%S''')}] {serverAnsw}")
        
            return serverAnsw
    
    def __checkConnection__(self):
        while True:
            if self.clientIsConnected:
                try:
                    self.send(msgValue = self.CHECK_CONNECTION_MESSAGE, msgKey = self.CHECK_CONNECTION_MESSAGE)
                except:
                    self.clientIsConnected = False
                    self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {self.ADDR} Server don't respond./n")
                    self.entryLog(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {self.ADDR} Server don't respond.]")
                    print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {self.ADDR} Server don't respond.")
                print("YES")
            else:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    self.client.connect(self.ADDR)
                    self.clientIsConnected = True
                    self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Connected to {self.SERVER}:{self.PORT}.../n")
                    self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Connected to {self.SERVER}:{self.PORT}...")
                    print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Connected to {self.SERVER}:{self.PORT}...")
                except:
                    self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Can't connect to {self.SERVER}:{self.PORT}.../n")
                    self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Can't connect to {self.SERVER}:{self.PORT}...")
                    print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Can't connect to {self.SERVER}:{self.PORT}...")


            time.sleep(0.1)

clnt = newClient()

clnt.start()
clnt.connect()


time.sleep(1)
clnt.send("Hello World!!")
time.sleep(5)
clnt.send("Hello Mike!")
time.sleep(20)

clnt.disconnect()
clnt.close()

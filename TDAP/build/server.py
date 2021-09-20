import time
import socket
import threading
from datetime import datetime

class newServer:
    HEADER = 64
    PORT = 55000
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "[DISCONNECT]"
    CHECK_CONNECTION_MESSAGE  = "[CHECK_CONNECTION]"
    TEXT_MESSAGE = "[TEXT]"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    entryLog = []
    clientList = []
    clientId = {}

    serverIsRunning = False
    activeClients = 0

    def __init__(self, __PORT__ = 55000):
        self.PORT = __PORT__
        
    def handle_client(self, conn, addr):
        self.clientId[addr] = True

        connected = True

        try:
            while connected and self.clientId.get(addr):

                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)

                if msg_length:
                    msg_length = int(msg_length)
                    msgKey, msgValue = str(conn.recv(msg_length).decode(self.FORMAT)).split(" --> ")


                    if msgKey == self.DISCONNECT_MESSAGE:
                        connected = False
                        conn.send("NONE".encode(self.FORMAT))
                    elif msgKey == self.CHECK_CONNECTION_MESSAGE:
                        conn.send(str(self.CHECK_CONNECTION_MESSAGE).encode(self.FORMAT))
                    elif msgKey == self.TEXT_MESSAGE:
                        self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgValue}/n")
                        self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgValue}")
                        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgValue}")
                        conn.send("NONE".encode(self.FORMAT))
                    else:
                        self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgKey} {msgValue}/n")
                        self.entryLog(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgKey} {msgValue}")
                        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgKey} {msgValue}")
                        conn.send("NONE".encode(self.FORMAT))
        except:
            self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Client don't respond./n")
            self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Client don't respond.")
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Client don't respond.")
        try:
            conn.close()
        except:
            pass

        if self.clientId.get(addr):
            self.clientId[addr] = False
            self.clientList.remove(addr)
            self.activeClients -= 1
            self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Disconnected by client. Active connections = {self.activeClients}/n")
            self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Disconnected by client. Active connections = {self.activeClients}")
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Disconnected by client. Active connections = {self.activeClients}")
            
    def __start__(self):
        try:
            self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARTING...] Server is starting.../n")
            self.entryLog(f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARTING...] Server is starting...")
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARTING...] Server is starting...")
            self.server.listen()
            self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [LISTENING] Server is listening on {self.SERVER}:{self.PORT}/n")
            self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [LISTENING] Server is listening on {self.SERVER}:{self.PORT}")
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [LISTENING] Server is listening on {self.SERVER}:{self.PORT}")

            while self.serverIsRunning:
                conn, addr = self.server.accept()
                self.clientList.append(addr)
                thread = threading.Thread(target = self.handle_client, args = (conn, addr), daemon = True)

                thread.start()

                
                self.activeClients += 1
                self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING] {addr} Active connections = {self.activeClients}/n")
                self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING] {addr} Active connections = {self.activeClients}")
                print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING] {addr} Active connections = {self.activeClients}")
        except:
            pass

    def start(self):
        self.serverIsRunning = True

        try:
            self.log = open(f"log-server-{self.SERVER}:{self.PORT}.txt", 'a')
        except:
            self.log = open(f"log-server-{self.SERVER}:{self.PORT}.txt", 'r+')

        self.entryLog = self.log.readlines()


        startServer = threading.Thread(target = self.__start__, args = (), daemon = True)
        startServer.start()

    def close(self):
        for clientIP in self.clientList:
            if self.clientId.get(clientIP) == True:
                self.clientId[clientIP] = False
                self.activeClients -= 1
                self.log.writeline((f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {clientIP} Disconnected by server. Active connections = {self.activeClients}/n")
                self.entryLog.append((f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {clientIP} Disconnected by server. Active connections = {self.activeClients}")
                print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {clientIP} Disconnected by server. Active connections = {self.activeClients}")
                time.sleep(1)

        self.clientList = []

        self.server.close()
        self.log.writeline(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]/n")
        self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]")
        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]")

srv = newServer()
srv.start()
time.sleep(159)
srv.close()

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
                        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgValue}")
                        conn.send("NONE".encode(self.FORMAT))
                    else:
                        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgKey} {msgValue}")
                        conn.send("NONE".encode(self.FORMAT))
        except:
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Client don't respond.")
        try:
            conn.close()
        except:
            pass

        if self.clientId.get(addr):
            self.clientId[addr] = False
            self.clientList.remove(addr)
            self.activeClients -= 1
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Disconnected by client. Active connections = {self.activeClients}")
            
    def __start__(self):
        try:
            print("[STARTING...] Server is starting...")
            self.server.listen()
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [LISTENING] Server is listening on {self.SERVER}:{self.PORT}")

            while self.serverIsRunning:
                conn, addr = self.server.accept()
                self.clientList.append(addr)
                thread = threading.Thread(target = self.handle_client, args = (conn, addr), daemon = True)

                thread.start()

                
                self.activeClients += 1
                print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING] {addr} Active connections = {self.activeClients}")
        except:
            pass

    def start(self):
        self.serverIsRunning = True

        startServer = threading.Thread(target = self.__start__, args = (), daemon = True)
        startServer.start()

    def close(self):
        for clientIP in self.clientList:
            if self.clientId.get(clientIP) == True:
                self.clientId[clientIP] = False
                self.activeClients -= 1
                print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {clientIP} Disconnected by server. Active connections = {self.activeClients}")
                time.sleep(1)

        self.clientList = []

        self.server.close()
        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]")

srv = newServer()
srv.start()
time.sleep(159)
srv.close()
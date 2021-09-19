import threading

from client import newClient
from server import newServer

srv = newServer()
clnt = newClient()


server = threading.Thread(target = srv.start, args = (), daemon=True)

server.start()
server.join()

clnt.connect()

while True:
    msg = input()

    if msg == clnt.DISCONNECT_MESSAGE:
        break
    else:
        clnt.send(msg)
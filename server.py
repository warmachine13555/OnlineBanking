import socket
import threading
from authentication import auth, register

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(("81.169.141.81", 8888))
server.bind(("localhost", 7777))
server.listen()

while True:
    client, addr = server.accept()
    threading.Thread(target=auth, args=(client,)).start()

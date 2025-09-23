import socket
import threading
import sys

clients = []

def handle_client(client_socket,addr,other_port):
    print(f"Connected to client {addr}")
    clients.append(client_socket)

    while True:
        msg = client_socket.recv(1024).decode()
        if not msg:
            break
        print(f"Received message from client: {msg}")

        broadcast_to_all_clients(msg,client_socket)

        if msg[0:7] != "FORWARD":
            send_to_other_server(msg,other_port)

    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()

def broadcast_to_all_clients(msg,sender):
    for client_socket in clients:
        if client_socket != sender:
            client_socket.send(msg.encode())

def send_to_other_server(msg,other_port):
    other_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    other_server.connect(('127.0.0.1',other_port))
    other_server.send(f"FORWARD: {msg}".encode())
    other_server.close()

server_num = sys.argv[1]

if server_num=="1":
    my_port = 5007
    other_port = 5008
else:
    my_port = 5008
    other_port = 5007


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1',my_port))
server_socket.listen(5)

while True:
    client_socket,addr = server_socket.accept()
    
    threading.Thread(target=handle_client,args=(client_socket,addr,other_port),daemon=True).start()

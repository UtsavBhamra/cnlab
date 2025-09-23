import socket
import threading

clients = []

def broadcast(msg,sender_socket):
    for socket in clients:
        if socket != sender_socket:
            socket.send(msg)

def handle_client(client_socket,addr):
    print(f"Accepted connection from {addr}")
    clients.append(client_socket)

    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print(f"msg = {msg}")
            broadcast(msg,client_socket)
        except:
            break
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1',12348))
    server_socket.listen(15)
    print("Server is listening on 127.0.0.1")

    while True:
        client_socket,addr = server_socket.accept()
        thread = threading.Thread(target=handle_client,args=(client_socket,addr))
        thread.start()

if __name__ == "__main__":
    start_server()
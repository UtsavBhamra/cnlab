import socket
import threading

def receive(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print(f"Received msg: {msg}")
        except:
            break

port = input("Enter the port of the server to connect to (5001 or 5002): ")
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1',int(port)))
print(f"Connected to port {port}")

threading.Thread(target=receive,args=(client_socket,),daemon=True).start()

while True:
    msg = input("Enter message: ")
    if msg.lower()=="exit":
        break
    client_socket.send(msg.encode())

client_socket.close()
import socket
import threading

def receive_tcp(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print(f"\nReceived: {msg}")
        except:
            break


def receive_udp(client_socket):
    while True:
        try:
            msg, addr = client_socket.recvfrom(1024)
            print(f"\nReceived from {addr}: {msg.decode()}")
        except:
            break


conn_type = input("Enter type of connection (1: TCP, 2: UDP): ")
port = int(input("Enter the server port to connect to: "))

if conn_type == "1":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', port))
    threading.Thread(target=receive_tcp, args=(client_socket,), daemon=True).start()

else:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # "connect" for UDP binds a default target for send()
    client_socket.connect(('127.0.0.1', port))
    threading.Thread(target=receive_udp, args=(client_socket,), daemon=True).start()

print("Connected.\n")

while True:
    msg = input("> ")
    if msg.lower() == "exit":
        break

    if conn_type == "1":
        client_socket.send(msg.encode())
    else:
        client_socket.sendto(msg.encode(), ('127.0.0.1', port))

print("Closing client.")
client_socket.close()

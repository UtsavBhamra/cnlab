import socket
import threading
import sys

clients = []  # For TCP: list of sockets, For UDP: list of (ip,port) tuples


def handle_tcp_client(client_socket, addr, conn_type, other_port):
    print(f"Connected to client {addr}\n")
    clients.append(client_socket)

    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print(f"Received message '{msg}' from {addr}")

            broadcast_tcp(msg, client_socket)

            if not msg.startswith("FORWARD"):
                forward_message(msg, other_port, conn_type)

        except:
            break

    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()


def broadcast_tcp(msg, sender_socket):
    for c in clients:
        if c != sender_socket:
            c.send(msg.encode())


def broadcast_udp(server_socket, msg, sender_addr):
    for addr in clients:
        if addr != sender_addr:
            server_socket.sendto(msg.encode(), addr)


def forward_message(msg, other_port, conn_type):
    if conn_type == "1":  # TCP forward
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', other_port))
        s.send(f"FORWARD: {msg}".encode())
        s.close()
    else:  # UDP forward
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(f"FORWARD: {msg}".encode(), ('127.0.0.1', other_port))
        s.close()


# ---------------- SERVER INIT -----------------

server_num = sys.argv[1]
conn_type = sys.argv[2]  # 1 = TCP, 2 = UDP

if server_num == "1" and conn_type == "1":
    my_port, other_port = 5021, 5022
elif server_num == "2" and conn_type == "1":
    my_port, other_port = 5022, 5021
elif server_num == "1" and conn_type == "2":
    my_port, other_port = 5023, 5024
else:
    my_port, other_port = 5024, 5023


# ---------------- SOCKET SETUP -----------------

if conn_type == "1":
    # TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', my_port))
    server_socket.listen()
else:
    # UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', my_port))

print(f"Listening on port {my_port} (Type: {'TCP' if conn_type=='1' else 'UDP'})\n")

# ---------------- MAIN LOOP -----------------

if conn_type == "1":  # TCP Server
    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_tcp_client,
                         args=(client_socket, addr, conn_type, other_port)).start()

else:  # UDP Server
    while True:
        msg, addr = server_socket.recvfrom(1024)
        msg = msg.decode()

        if not msg.startswith("FORWARD") and addr not in clients:
            print(f"Adding {addr} to clients")
            clients.append(addr)

        print(f"Received '{msg}' from {addr}")

        broadcast_udp(server_socket, msg.replace("FORWARD: ",""), addr)

        if not msg.startswith("FORWARD"):
            forward_message(msg, other_port, conn_type)

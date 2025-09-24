import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5002))

while True:
    passwd = input("Enter a password (or 'quit' to exit): ")

    if passwd.lower() == "quit":
        break

    client_socket.send(passwd.encode())
    response = client_socket.recv(1024).decode()
    print("Server:", response)

client_socket.close()

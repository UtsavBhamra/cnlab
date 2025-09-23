import socket 
import threading

def handle_client(client_socket,addr):
    print(f"Connected to client {addr}\n")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"message from client = {message}")
            client_socket.send(message.encode())
        except:
            break
    print(f"Disconnected from {addr}")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1',12345))
    server_socket.listen(5)
    print("server is listening on 127.0.0.1 at port 12345\n")

    while True:
        client_socket,addr = server_socket.accept()
        thread = threading.Thread(target=handle_client,args=(client_socket,addr))
        thread.start()

if __name__ == "__main__":
    start_server()
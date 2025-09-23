import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1',12345))

    print("Client is now connected to server. Type 'exit' to exit: ")

    while True:
        message = input("You: ")
        if message.lower() == "exit":
            break
        client_socket.send(message.encode())
        echo = client_socket.recv(1024).decode()

        print(f"echo = {echo}")

    client_socket.close()

if __name__ == "__main__":
    start_client()




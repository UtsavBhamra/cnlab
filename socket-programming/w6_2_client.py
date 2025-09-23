import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    client_socket.connect(('127.0.0.1',12347))
    print("Client established connection with server. Enter City or type (exit): ")

    while True:
        city = input("City: ")
        if city.lower() == "exit":
            break
        client_socket.send(city.encode())
        weather = client_socket.recv(1024).decode()
        print(f"Weather: {weather}")
    
    client_socket.close()

if __name__ == "__main__":
    start_client()

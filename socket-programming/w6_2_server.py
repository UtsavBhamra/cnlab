import socket
import threading

weather_dict = {"Mumbai":"Sunny","Bengaluru":"Cloudy","Delhi":"Rain","Chennai":"Sunny"}

def handle_client(client_socket,addr):
    print(f"Accepted connection from client {addr}")

    while True:
        try:
            city = client_socket.recv(1024).decode()
            if not city:
                break
            if city in weather_dict:
                client_socket.send(weather_dict[city].encode())
            else:
                client_socket.send("City weather data is not available".encode())
        except:
            break

    print("Disconnected from client: {addr}")
    client_socket.close()



def start_server():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1',12347))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client,args=(client_socket,addr))
        thread.start()

if __name__ == "__main__":
    start_server()
    

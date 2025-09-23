import socket
import threading

HOST = "127.0.0.1"
PORT = 12348

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print("\n" + msg)
        except:
            break

def send(sock):
    while True:
        msg = input()
        sock.send(msg.encode())

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    threading.Thread(target=receive, args=(client,), daemon=True).start()
    send(client)

if __name__ == "__main__":
    main()

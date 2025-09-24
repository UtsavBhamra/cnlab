import socket
import threading

def handle_client(client_socket, addr):
    print(f"Connected to client {addr}")

    while True:
        try:
            passwd = client_socket.recv(1024).decode()
            if not passwd:
                break

            # Flags
            len_flag = 0
            lower_case_flag = 0
            upper_case_flag = 0
            digit_flag = 0
            special_char_flag = 0

            if 8 <= len(passwd) <= 20:
                len_flag = 1

            digits = "0123456789"
            special = "_@$"

            for ch in passwd:
                if ch.islower():
                    lower_case_flag = 1
                if ch.isupper():
                    upper_case_flag = 1
                if ch in digits:
                    digit_flag = 1 
                if ch in special:
                    special_char_flag = 1

            if all([len_flag, lower_case_flag, upper_case_flag, digit_flag, special_char_flag]):
                client_socket.send("Valid password".encode())
            else:
                client_socket.send("Invalid password".encode())
        except Exception as e:
            print("Error:", e)
            break

    print("Closing client connection")
    client_socket.close()


# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5002))
server_socket.listen(10)
print("Server is listening on port 5002")

while True:
    client_socket, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()

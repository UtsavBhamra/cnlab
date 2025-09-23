import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('127.0.0.1',12348))

s.listen()
print("Server is listening on 127.0.0.1 at port 12348\n")

c,addr = s.accept()
print("Accepted connection from ",addr,"\n")


while(1):
    data = c.recv(1024).decode()
    arr = data.split(" ")

    if len(arr)!=3:
        c.send("Invalid input format".encode())

    result = None
    op1 = float(data[0])
    op2 = float(data[2]) 

    if data[1]=="+":
        result = op1+op2
    elif data[1]=="-":
        result = op1-op2
    elif data[1]=="*":
        result = op1*op2
    elif data[1]=="/":
        result = op1/op2
    else:
        result = "Invalid input"

    ans = "Server: "+str(result)
    c.send(ans.encode())

import threading
import socket

HOST = '127.0.0.1'
PORT = 49474

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object (AF_INET: address family, SOCK_STREAM: socket type)

try:
    s.connect((HOST, PORT))  # Connect to the server
except ConnectionRefusedError:
    print("Connection is not find")
    exit()

while True:
    try:
        msg = s.recv(512).decode("utf-8") # Receive data from the server
        attr = msg.split(" ")
        if attr[0] == "PAS":
            nickname = input("Input a password --> ")
            s.send(nickname.encode("utf-8"))
        elif attr[0] == "COM":
            command = input("Input a command (type 'HELP' to show all commands) --> ")
            s.send(command.encode("utf-8"))
        elif attr[0] == "DIS":
            print("Quiting...")
            break
        elif attr[0] == "MES":
            print(" ".join(attr[1:]))
    except ConnectionResetError:
        print("Server is not responding")
        break
import threading
import socket
import netifaces

HOST, PORT = input("Input a address --> ").split(":")
cookies = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object (AF_INET: address family, SOCK_STREAM: socket type)

try:
    s.connect((HOST, int(PORT)))  # Connect to the server
except ConnectionRefusedError:
    print("Connection is not find")
    exit()
except ValueError:
    print("Input a correct port")
    exit()
except socket.gaierror:
    print("Input a correct address")
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
            s.send(f"{cookies} {command}".encode("utf-8"))
        elif attr[0] == "DIS":
            print("Quiting...")
            break
        elif attr[0] == "MES":
            print(" ".join(attr[1:]))
        elif attr[0] == "COOK":
            cookies = attr[1]
            print("Cookies set")
            s.send("SUCCESS".encode("utf-8"))
            command = input("Input a command (type 'HELP' to show all commands) --> ")
            s.send(f"{cookies} {command}".encode("utf-8"))
    except ConnectionResetError:
        print("Server is not responding")
        break
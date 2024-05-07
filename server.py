import threading
import socket
import webbrowser
from hashlib import sha256

HOST = '127.0.0.1'
PORT = 49474

# password from password.txt
PASSWORD = open("password.txt", "r").read()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object (AF_INET: address family, SOCK_STREAM: socket type)

server.bind((HOST, PORT))  # Bind the socket to the address and port
server.listen()  # Listen for incoming connections

clients = []

def go_to_page(url):
    webbrowser.open(url)

def set_volume(volume: float) -> str:
    return f""

HELP_STR = '''
Commands:
'HELP' - show all commands,
'URL [-url]' - open the URL in the browser
    Options:
        -url     url adress
'VOL [-volume] [-name]' - set the volume of the application
    Options:
        -volume  volume level
        -name    name of the application
'''

def handle(client):
    while True:
        try:
            command = client.recv(1024)
            # Split the message by spacing
            attributes = command.decode("utf-8").split(" ")
            if attributes[0] == "HELP":
                client.send(f"MES {HELP_STR}".encode("utf-8"))
            elif attributes[0] == "URL":
                go_to_page(attributes[1])
                client.send("MES URL is opened!".encode("utf-8"))
            elif attributes[0] == "VOL":
                mes_ret = set_volume(attributes[1], attributes[2])
                client.send(f"MES {mes_ret}".encode("utf-8"))
            client.send("COM".encode("utf-8"))
        except:
            clients.remove(client)
            client.close()
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with{address}")

        client.send("PAS".encode("utf-8"))
        password = client.recv(1024).decode("utf-8")
        if sha256(password.encode("utf-8")).hexdigest() != PASSWORD:
            client.send("DIS".encode("utf-8"))
            client.close()
            continue

        clients.append(client)

        print(f"Client connected: {client}")
        client.send("Connected to the server!".encode("utf-8"))
        client.send("COM".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
if __name__ == "__main__":
    receive()
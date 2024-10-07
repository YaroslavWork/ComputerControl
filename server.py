import threading
import socket
import webbrowser
from hashlib import sha256
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os

HOST, PORT = open("host.txt", "r").read().split(":")

# password from password.txt
PASSWORD = open("password.txt", "r").read()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object (AF_INET: address family, SOCK_STREAM: socket type)

server.bind((HOST, int(PORT)))  # Bind the socket to the address and port
server.listen()  # Listen for incoming connections

clients = []
cookies = []

def go_to_page(url):
    webbrowser.open(url)

def set_global_volume(level) -> str:
    # Get the default audio device
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    # Cast the interface to a pointer to IAudioEndpointVolume
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Set the volume level (0.0 to 1.0)
    volume.SetMasterVolumeLevelScalar(level, None)
    return "Volume is set"

def move_offset(x: int, y: int) -> str:
    pyautogui.move(x, y)
    return "Mouse moved"

def click() -> str:
    pyautogui.click()
    return "Mouse clicked"

HELP_STR = '''
Commands:
'HELP' - show all commands,
'URL [-url]' - open the URL in the browser
    Options:
        -url     url adress
'VOL [-volume]' - set the volume of the application
    Options:
        -volume  volume level
'''

def handle(client):
    while True:
        try:
            command = client.recv(1024)
            # Split the message by spacing
            attributes = command.decode("utf-8").split(" ")
            if attributes[0] in cookies:
                if attributes[1] == "HELP":
                    client.send(f"MES {HELP_STR}".encode("utf-8"))
                elif attributes[1] == "URL":
                    go_to_page(attributes[2])
                    client.send("MES URL is opened!".encode("utf-8"))
                elif attributes[1] == "VOL":
                    mes_ret = set_global_volume(float(attributes[2]))
                    client.send(f"MES {mes_ret}".encode("utf-8"))
                elif attributes[1] == "MOV":
                    mes_ret = move_offset(int(attributes[2]), int(attributes[3]))
                    client.send(f"MES {mes_ret}".encode("utf-8"))
                elif attributes[1] == "CLK":
                    mes_ret = click()
                    client.send(f"MES {mes_ret}".encode("utf-8"))
                elif attributes[1] == "LOCK":
                    os.system("rundll32.exe user32.dll,LockWorkStation")
                elif attributes[1] == "SHUT":
                    if len(attributes) > 1:
                        os.system(f"shutdown /s /t {attributes[2]}")
                    else:
                        os.system("shutdown /s /t 1")
                client.send("COM".encode("utf-8"))
        except:
            clients.remove(client)
            cookies.remove(client)
            client.close()
            print(f"Client disconnected: {client}")
            break

def auth(client, sha_password: str) -> None:
    while True:
        client.send("PAS".encode("utf-8"))
        password = client.recv(1024).decode("utf-8")
        if sha256(password.encode("utf-8")).hexdigest() != sha_password:
            client.send("DIS".encode("utf-8"))
            client.close()
            print(f"Client disconnected: {client}")
            continue
        clients.append(client)
        cookie = sha256(str(os.urandom(1024)).encode("utf-8")).hexdigest()
        cookies.append(cookie)

        print(f"Client authenticated: {client}")
        client.send("MES Connected to the server!".encode("utf-8"))
        client.send(f"COOK {cookie}".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        break

def receive():
    while True:
        client, address = server.accept()
        print(f"This address connecting: {address}")

        thread = threading.Thread(target=auth, args=(client, PASSWORD))
        thread.start()


print(f"Server is listening on {HOST}:{PORT}")
if __name__ == "__main__":
    receive()
    print(sha256("123".encode("utf-8")).hexdigest())
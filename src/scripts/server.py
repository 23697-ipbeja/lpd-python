import threading
import socket
from datetime import datetime
import sys
import rsa

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 

public_key, private_key = rsa.newkeys(1024)
public_partner = None

host = '127.0.0.1'
port = 55555


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("Server is listening...")
(conn, addr) = server.accept()

conn.send(public_key.save_pkcs1("PEM"))
public_partner = rsa.PublicKey.load_pkcs1(conn.recv(1024))

conn.send(rsa.encrypt('NICK'.encode(), public_partner))
nickname = rsa.decrypt(conn.recv(1024), private_key).decode()
print(f'{nickname} from {addr} is connected\n')

def receive():
    while True:
        message = rsa.decrypt(conn.recv(1024), private_key).decode()
        saveFile(nickname, str(message))
        print(message)


def write():
    while True:
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        message = f'\033[1;32m[{timestamp}]\u001b[0m - Server: {input("")}'
        saveFile(nickname, str(message))
        sys.stdout.write(CURSOR_UP_ONE) 
        sys.stdout.write(ERASE_LINE)  
        conn.send(rsa.encrypt(message.encode(), public_partner))
        print(message)

def saveFile(nickname, data):
    now = datetime.now()
    timestamp = now.strftime("%d%m%y")
    f = open("./export/" + nickname + "_" + timestamp + ".txt", "a")
    f.write(data + '\n')
    f.close()

receive_thread = threading.Thread(target=receive).start()
write_thread = threading.Thread(target=write).start()

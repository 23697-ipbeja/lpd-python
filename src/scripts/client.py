import socket
import threading
from datetime import datetime
import sys
import rsa

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 

public_key, private_key = rsa.newkeys(1024)
public_partner = None

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
client.send(public_key.save_pkcs1("PEM"))

def receive():
    while True:
        try:
            message = rsa.decrypt(client.recv(1024), private_key).decode()
            if message == 'NICK':
                client.send(rsa.encrypt(nickname.encode(), public_partner))
                print(f'{nickname} is Connected to Server\n')
            else:
                print(message)
        except:
            print(f"{nickname} is disconnected")
            client.close()
            break

def write():
    while True:
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        message = (f'\033[1;32m[{timestamp}]\u001b[0m - {nickname}: {input("")}')
        sys.stdout.write(CURSOR_UP_ONE) 
        sys.stdout.write(ERASE_LINE)
        client.send(rsa.encrypt(message.encode(), public_partner)) 
        print(message)


receive_thread = threading.Thread(target=receive).start()
write_thread = threading.Thread(target=write).start()




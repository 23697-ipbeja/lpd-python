import socket
import threading
from datetime import datetime
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))
public_key = client.recv(4096)

key = RSA.importKey(public_key)

# Encryption
cipher = PKCS1_OAEP.new(key)

# Decryption
decipher = PKCS1_OAEP.new(key)


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                print(f'{nickname} is Connected to Server')
            else:
                encrypted_data = client.recv(4096)
                decrypted_data = decipher.decrypt(encrypted_data)
                print(decrypted_data.decode())
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        message = (f'\033[1;32m[{timestamp}]\u001b[0m - {nickname}: {input("")}')
        sys.stdout.write(CURSOR_UP_ONE) 
        sys.stdout.write(ERASE_LINE) 
        print(message)
        message = message.encode()
        encrypted_message = cipher.encrypt(message)
        client.send(encrypted_message)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()



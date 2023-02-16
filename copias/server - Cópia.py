import threading
import socket
from datetime import datetime
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 

host = '127.0.0.1'
port = 55555

# Generate a 2048-bit RSA key
key = RSA.generate(2048)

# Encryption
cipher = PKCS1_OAEP.new(key)

# Decryption
decipher = PKCS1_OAEP.new(key)

# Get the public key to send to the client
public_key = key.publickey().exportKey()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("Server is listening...")
(conn, addr) = server.accept()
conn.send(public_key)
conn.send('NICK'.encode('ascii'))
nickname = conn.recv(1024).decode('ascii')
print(f'{nickname} from {addr} is connected')


clients = []
nicknames = []

def receive():
    while True:
        encrypted_data = conn.recv(4096)
        decrypted_data = decipher.decrypt(encrypted_data)
        print(decrypted_data.decode())


def write():
    while True:
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        message = f'\033[1;32m[{timestamp}]\u001b[0m - Server: {input("")}'
        sys.stdout.write(CURSOR_UP_ONE) 
        sys.stdout.write(ERASE_LINE)  
        print(message)
        conn.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

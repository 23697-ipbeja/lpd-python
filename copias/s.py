# Server

import socket
import threading
import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

client, _ = server.accept()
client.send(public_key.save_pkcs1("PEM"))
public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)

def receiving_messages(c):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(1024), private_key).decode())

threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
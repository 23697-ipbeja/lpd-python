from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

# Receive public key from server
public_key = client_socket.recv(4096)

key = RSA.importKey(public_key)

# Encryption
cipher = PKCS1_OAEP.new(key)

# Decryption
decipher = PKCS1_OAEP.new(key)

# Encrypt the message to send to the server
message = "This is Client".encode()
encrypted_message = cipher.encrypt(message)

# Send encrypted message to the server
client_socket.send(encrypted_message)
encrypted_data = client_socket.recv(4096)
message = decipher.decrypt(encrypted_data)
print(message.decode())
client_socket.close()

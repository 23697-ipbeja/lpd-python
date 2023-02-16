from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(1)
print("Listening on port 5000")

# Generate a 2048-bit RSA key
key = RSA.generate(2048)

# Encryption
cipher = PKCS1_OAEP.new(key)

# Decryption
decipher = PKCS1_OAEP.new(key)

# Get the public key to send to the client
public_key = key.publickey().exportKey()

conn, client_address = server_socket.accept()
print("Accepted connection from:", client_address)

conn.send(public_key)

# Receive encrypted message from client
encrypted_data = conn.recv(4096)

# Decrypt the message
decrypted_data = decipher.decrypt(encrypted_data)

print("Received message:", decrypted_data.decode())


message = "This is Server".encode()
encrypted_data = cipher.encrypt(message)
conn.send(encrypted_data)

conn.close()

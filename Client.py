import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os
from file_encryption import *
from lsb_stegno import *
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))  # Connect to the server

# Receive the RSA public key from the server for key exchange
server_public_key = None
public_key_pem = client_socket.recv(4096)
iv=client_socket.recv(4096)
server_public_key = serialization.load_pem_public_key(
    public_key_pem,
    backend=default_backend()
)

# Read the file to be encrypted
# input_file = 'file_to_embed.txt'
input_file = input("Enter the file to be encrypted: ")
input_image = input("Enter the image: ")
# Generate a random AES key
aes_key = os.urandom(32)  # 256-bit key for AES-256
print("AES_Key: ",aes_key)

#Encrypt file using AES
file_data=encrypt_text(input_file,aes_key,iv)
print("Encrypted_file_data: ",file_data)
#embed the file into image
image = embed(input_image,file_data)
encrypted_aes_key=rsa_encrypt(aes_key,server_public_key)

print("encrypted_aes_key: ",encrypted_aes_key)
# Send the encrypted file and AES key to the server
client_socket.send(encrypted_aes_key)
client_socket.send(image)


print("Encrypted file has been sent to server!!.")
client_socket.close()  # Close the client connection

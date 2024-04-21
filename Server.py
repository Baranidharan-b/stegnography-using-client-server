import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from Crypto.Random import get_random_bytes
from file_encryption import *
from lsb_stegno import *
# Generate RSA key pair for AES key encryption
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# Generate a random IV of the appropriate size for AES (16 bytes for AES-128)
iv = get_random_bytes(AES.block_size)

# Serialize the public key for encryption
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
server_socket.listen(1)  # Listen for incoming connections

print("Server is listening...")

while True:
    client_socket, client_addr = server_socket.accept()  # Accept incoming connection
    print(f"Connection from {client_addr}")

    # Send the public key to the client for key exchange
    client_socket.send(public_key_pem)
    client_socket.send(iv)

    # Receive the AES-encrypted file from the client
    image_data = b""
    encrypted_aes_key = client_socket.recv(4096)
    while True:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        image_data += chunk

    with open("received_image.png", "wb") as file:
        file.write(image_data)

    # encrypted_file = client_socket.recv(4096)
    # encrypt_file=encrypted_file.decode('utf-8')
    # print("Encrypted_file: ",encrypt_file)

    # Decrypt AES key using RSA private key

    print("encrypted_aes_key: ", encrypted_aes_key)
    aes_key = rsa_decrypt(encrypted_aes_key,private_key)
    print("Decrepted AES key: ",aes_key)
    encrypted_file=extract("received_image.png")
    print("Extracted_file_data: ", encrypted_file)
    decrypted_data=decrypt_text(encrypted_file,aes_key,iv)

    print("Decrypted_Data: ",decrypted_data)
    # Write decrypted data to a new file
    with open('decrypted_file.txt', 'w') as f:
        f.write(decrypted_data)

    print("File decrypted and saved.")
    client_socket.close()  # Close the client connection

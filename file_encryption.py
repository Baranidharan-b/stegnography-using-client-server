from Crypto.Util.Padding import pad, unpad
import base64
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
#Encryption
def rsa_encrypt(info, key):
    aes_key=info
    server_public_key=key
    encrypted_aes_key = server_public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_aes_key

def rsa_decrypt(info, key):
    encrypted_aes_key=info
    private_key=key
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return aes_key
def encrypt_text(input_file,key,iv):
    with open(input_file, 'r') as f:
        plaintext = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plaintext.encode(), AES.block_size)  # Ensure text is in bytes format
    encrypted_text = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted_text).decode()  # Convert bytes to base64 encoded string

# Decryption function
def decrypt_text(encrypted_text,key,iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = cipher.decrypt(base64.b64decode(encrypted_text))
    return unpad(decrypted_text, AES.block_size).decode()
#
# def aes_encrypt(info,encrypt_key):
#     msg = info
#     key = encrypt_key
#     Block_size = 128
#     pad = "{"
#     padding = lambda s: s + (Block_size - len(s) % Block_size) * pad
#     cipher = AES.new(key,AES.MODE_ECB)
#     result = cipher.encrypt(padding(msg).encode('utf-8'))
#     return result
#
#
# #Decryption
# def aes_decrypt(info,decrypt_key):
#     msg=info
#     key = decrypt_key
#     PAD = "{"
#     decipher = AES.new(key,AES.MODE_ECB)
#     pt = decipher.decrypt(msg).decode('utf-8')
#     pad_index = pt.find(PAD)
#     result = pt[:pad_index]
#     return result

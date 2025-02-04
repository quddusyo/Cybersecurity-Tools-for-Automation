'''
req: pip install cryptography (windows)
sudo apt install build-essential libssl-dev python3-dev
pip install cryptography (linux)
Additionally, you may need to chmod +x encrypt_aes.py
Useage: python ransom_air.py
'encrypt' or 'decrypt'
Then provide your path of directory you would like to encrypt/decrypt.
Then provide a password for the encryption/decryption.

Script to encrypt files. Works on both Linux and Windows OS.

Description: This script encrypts files and folder names within 
a specified directory using AES (Advanced Encryption Standard) in 
CBC (Cipher Block Chaining) mode, with encryption keys derived from 
a user-provided password through the PBKDF2 key derivation function. 
It first generates a unique salt and initialization vector (IV) for 
each encryption process, pads the data to meet AES block size 
requirements, and then encrypts the content of each file. After 
encryption, the salt and IV are stored in the encrypted file for 
decryption purposes. Folder and file names are also encrypted and 
renamed to their encrypted counterparts. If an incorrect password is 
used during decryption, the process will fail with a padding error due 
to an invalid decryption key. The script can handle such errors 
gracefully, informing the user that the password might be incorrect.
'''

import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding, hashes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import secrets

# Derive a key from a password using PBKDF2
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 needs a 32-byte key
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Function to pad the data to match AES block size (16 bytes)
def pad_data(data):
    padder = padding.PKCS7(128).padder()  # AES block size is 128 bits (16 bytes)
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

# Function to unpad the decrypted data
def unpad_data(padded_data):
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

# Function to encrypt a file using AES
def encrypt_file(file_path, key, salt):
    iv = secrets.token_bytes(16)  # Generate a random 16-byte IV

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, "rb") as file:
        original_data = file.read()

    padded_data = pad_data(original_data)  # Pad data to be AES block size (16 bytes)

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Write the encrypted data back to the file, with the salt and IV prepended
    with open(file_path, "wb") as encrypted_file:
        encrypted_file.write(salt + iv + encrypted_data)

    print(f"Encrypted file: {file_path}")

# Function to encrypt folder and file names
def encrypt_name(name, key):
    iv = secrets.token_bytes(16)  # Generate a random 16-byte IV for the name

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    name_bytes = name.encode("utf-8")
    padded_name = pad_data(name_bytes)

    encrypted_name = encryptor.update(padded_name) + encryptor.finalize()

    encrypted_name_b64 = urlsafe_b64encode(iv + encrypted_name).decode("utf-8")
    
    return encrypted_name_b64

# Function to decrypt a file using AES
def decrypt_file(file_path, password):
    with open(file_path, "rb") as encrypted_file:
        file_data = encrypted_file.read()

    # Extract the salt (first 16 bytes), IV (next 16 bytes), and encrypted data
    salt = file_data[:16]
    iv = file_data[16:32]
    encrypted_data = file_data[32:]

    # Derive the key from the password and salt
    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    original_data = unpad_data(padded_data)

    with open(file_path, "wb") as decrypted_file:
        decrypted_file.write(original_data)

    print(f"Decrypted file: {file_path}")

# Function to decrypt folder and file names
def decrypt_name(encrypted_name_b64, key):
    encrypted_name_bytes = urlsafe_b64decode(encrypted_name_b64)

    iv = encrypted_name_bytes[:16]
    encrypted_name = encrypted_name_bytes[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_name = decryptor.update(encrypted_name) + decryptor.finalize()

    original_name = unpad_data(padded_name).decode("utf-8")

    return original_name

# Function to recursively encrypt files and folder names
def encrypt_directory(directory_path, password):
    salt = secrets.token_bytes(16)  # Generate a salt for key derivation (16 bytes)

    key = derive_key(password, salt)  # Derive the AES key from the password and salt

    for root, dirs, files in os.walk(directory_path, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            encrypt_file(file_path, key, salt)

            encrypted_file_name = encrypt_name(file_name, key)
            encrypted_file_path = os.path.join(root, encrypted_file_name)
            if not os.path.exists(encrypted_file_path):
                os.rename(file_path, encrypted_file_path)

            print(f"Encrypted filename: {file_path} -> {encrypted_file_path}")

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            encrypted_dir_name = encrypt_name(dir_name, key)
            encrypted_dir_path = os.path.join(root, encrypted_dir_name)
            os.rename(dir_path, encrypted_dir_path)

            print(f"Encrypted folder name: {dir_path} -> {encrypted_dir_path}")

# Function to recursively decrypt files and folder names
def decrypt_directory(directory_path, password):
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "rb") as file:
                salt = file.read(16)  # Extract the salt from the first 16 bytes
            key = derive_key(password, salt)

            decrypt_file(file_path, password)

            decrypted_file_name = decrypt_name(file_name, key)
            decrypted_file_path = os.path.join(root, decrypted_file_name)
            if not os.path.exists(decrypted_file_path):
                os.rename(file_path, decrypted_file_path)

            print(f"Decrypted filename: {file_path} -> {decrypted_file_path}")

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            decrypted_dir_name = decrypt_name(dir_name, key)
            decrypted_dir_path = os.path.join(root, decrypted_dir_name)
            os.rename(dir_path, decrypted_dir_path)

            print(f"Decrypted folder name: {dir_path} -> {decrypted_dir_path}")

if __name__ == "__main__":
    operation = input("Enter 'encrypt' to encrypt or 'decrypt' to decrypt: ")
    directory_to_process = input("Enter the directory to process: ")
    password = input("Enter the password: ")

    if os.path.isdir(directory_to_process):
        if operation == "encrypt":
            encrypt_directory(directory_to_process, password)
            print("Encryption completed.")
        elif operation == "decrypt":
            decrypt_directory(directory_to_process, password)
            print("Decryption completed.")
        else:
            print("Invalid operation. Choose 'encrypt' or 'decrypt'.")
    else:
        print("Invalid directory path.")

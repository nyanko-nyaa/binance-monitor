import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_key():
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(b"default_password"))

    with open('salt.bin', 'wb') as salt_file:
        salt_file.write(salt)

    return key


def encrypt(data: str):
    key = generate_key()
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())


def decrypt(encrypted_data: bytes):
    with open('salt.bin', 'rb') as salt_file:
        salt = salt_file.read()

    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    fernet = Fernet(base64.urlsafe_b64encode(key))
    return fernet.decrypt(encrypted_data).decode()
from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes


class AESEncryption:
    @staticmethod
    def encrypt(password, text):
        salt = get_random_bytes(16)
        key = PBKDF2(password, salt, dkLen=32)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(text.encode())

        ciphertext = b64encode(ciphertext).decode("utf-8")

        return salt, cipher.nonce, ciphertext

    @staticmethod
    def decrypt(password, salt, nonce, ciphertext):
        ciphertext = b64decode(ciphertext.encode("utf-8"))

        key = PBKDF2(password, salt, dkLen=32)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt(ciphertext).decode()


__all__ = ["AESEncryption"]

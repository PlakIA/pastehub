from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def aes256_encrypt(key, plaintext):
    key = pad(key.encode("utf-8"), 32)[:32]
    plaintext = pad(plaintext.encode("utf-8"), 16)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = iv + cipher.encrypt(plaintext)

    return b64encode(ciphertext).decode("utf-8")


def aes256_decrypt(key, ciphertext):
    decoded_ciphertext = b64decode(ciphertext.encode("utf-8"))

    key = pad(key.encode("utf-8"), 32)[:32]
    iv = decoded_ciphertext[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(decoded_ciphertext[16:])

    return unpad(plaintext, 16).decode("utf-8")


__all__ = ["aes256_encrypt", "aes256_decrypt"]

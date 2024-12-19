from django.test import TestCase

from core.crypto import AESEncryption


class TestCrypto(TestCase):
    def test_encrypt_decrypt(self):
        key = "TeStKeY_123456!"
        input_text = "Test input text"

        salt, nonce, ciphertext = AESEncryption.encrypt(key, input_text)
        decrypted_text = AESEncryption.decrypt(key, salt, nonce, ciphertext)

        self.assertEqual(input_text, decrypted_text)


__all__ = []

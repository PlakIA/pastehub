from django.test import TestCase

from core.crypto import aes256_decrypt, aes256_encrypt


class TestCrypto(TestCase):
    def test_encrypt_decrypt(self):
        key = "TeStKeY_123456!"
        input_text = "Test input text"

        crypted_text = aes256_encrypt(key, input_text)
        decrypted_text = aes256_decrypt(key, crypted_text)

        self.assertEqual(input_text, decrypted_text)


__all__ = []

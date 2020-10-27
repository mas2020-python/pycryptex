from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES


class AESCryptex:
    def __init__(self):
        self.key: bytes = None
        self.salt: bytes = None

    def encrypt_data(self, clear_data: bytes, pwd: str) -> bytes:
        """
        This example do the following:
        - generate a salt
        - encrypt the clear_data

        :param clear_data: list of bytes to encrypt
        :param pwd: password to encrypt
        :return: encrypted bytes
        """
        if self.salt is None:
            self.salt = get_random_bytes(32)
            self.key = PBKDF2(pwd, self.salt, dkLen=32)  # the key that you can encrypt with
        cipher_aes = AES.new(self.key, AES.MODE_EAX)  # EAX mode
        # Encrypt and digest to get the ciphered data and tag
        ciphered_data, tag = cipher_aes.encrypt_and_digest(clear_data)

        encbytes_out = bytearray()
        for x in (self.salt, cipher_aes.nonce, tag, ciphered_data):
            encbytes_out.extend(x)
        return bytes(encbytes_out)

    def decrypt_data(self, enc_data: bytes, pwd: str) -> bytes:
        """
        This example do the following:
        - retrieve the salt
        - decrypt the clear_data

        :param enc_data: list of bytes to decrypt
        :param pwd: password to encrypt
        :return: decrypted bytes
        """
        if self.salt is None:
            self.salt = enc_data[:32]
            self.key = PBKDF2(pwd, self.salt, dkLen=32)  # the key that you can decrypt with
        # salt = enc_data[:32]
        nonce = enc_data[32:48]
        tag = enc_data[48:64]
        ciphered_data = enc_data[64:]
        # generate the key
        # key = PBKDF2(pwd, salt, dkLen=32)  # the key that you can encrypt with

        cipher = AES.new(self.key, AES.MODE_EAX, nonce)
        original_data = cipher.decrypt_and_verify(ciphered_data, tag)
        return original_data


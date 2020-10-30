"""
This module is useful to encrypt and decrypt using RSA algorithm.
"""
import os
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


class RSACryptex:
    def __init__(self):
        self.recipient_key: RSA.RsaKey = None
        self.session_key = None
        self.cipher_rsa = None
        self.enc_session_key = None

    def encrypt_data(self, clear_data: bytes, public_key: str) -> bytes:
        """
        This example do the following:
        - read the public key
        - create a random AES key of 128 bits
        - encrypt the AES key with the public key
        - encrypt data with the AES key (as the traditional symmetric algorithm does)
        - then write in a file the following information:
          - encrypted AES key (first 16 bits)
          - nonce utilized from the AES cypher
          - tag of the AES cypher
          - AES cypher bytes

        :param clear_data: list of bytes to encrypt
        :param public_key: RSA key used for encryption
        :return: encrypted bytes
        """
        encbytes_out = list()
        # if the key exist don't read
        if self.recipient_key is None:
            self.recipient_key = RSA.import_key(open(public_key).read())
            self.session_key = get_random_bytes(32)

            # Encrypt the session key with the public RSA key
            self.cipher_rsa = PKCS1_OAEP.new(self.recipient_key)
            self.enc_session_key = self.cipher_rsa.encrypt(self.session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(self.session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(clear_data)
        encbytes_out = bytearray()
        for x in (self.enc_session_key, cipher_aes.nonce, tag, ciphertext):
            encbytes_out.extend(x)
        return bytes(encbytes_out)

    def decrypt_data(self, enc_data: bytes, private_key: str, passprhase=None) -> bytes:
        """
        Decrypt data doing the following:
        - get encrypted key and nonce and tag + decrypted bytes
        - decrypt the AES encrypted key using the private key
        - use the AES keys and other information to decrypt data

        :param enc_data: encrypted bytes
        :param private_key: RSA private key used for decryption
        :return: list of decrypted bytes
        """
        # load the RSA private key
        if self.recipient_key is None:
            self.recipient_key = RSA.import_key(open(private_key).read(), passphrase=passprhase)
            # Decrypt the session key with the private RSA key
            self.cipher_rsa = PKCS1_OAEP.new(self.recipient_key)
            # get AES encrypted key
            enc_session_key = enc_data[:self.recipient_key.size_in_bytes()]
            # decrypt AES key
            self.session_key = self.cipher_rsa.decrypt(enc_session_key)

        # get the single elements from bytes list
        nonce = enc_data[self.recipient_key.size_in_bytes():self.recipient_key.size_in_bytes() + 16]
        tag = enc_data[self.recipient_key.size_in_bytes() + 16:self.recipient_key.size_in_bytes() + 32]
        ciphertext = enc_data[self.recipient_key.size_in_bytes() + 32:]

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(self.session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data

    @classmethod
    def create_keys(cls, folder: str, passprhase=None):
        """
        Create a public key and private key pair
        :param folder: directory where to create the pycryptex_key and pycryptex_key.pub files
        :return: None
        """
        key = RSA.generate(2048)
        private_key = None
        if passprhase:
            private_key = key.export_key(passphrase=passprhase, pkcs=8,
                                         protection="scryptAndAES128-CBC")
        else:
            private_key = key.export_key()

        with open(os.path.join(folder, "pycryptex_key"), "wb") as file_out:
            file_out.write(private_key)

        public_key = key.publickey().export_key()
        with open(os.path.join(folder, "pycryptex_key.pub"), "wb") as file_out:
            file_out.write(public_key)

    @classmethod
    def is_privatekey_protected(cls, key_file: str) -> bool:
        try:
            private_key = RSA.import_key(open(key_file).read(), passphrase="")
            public_key = private_key.publickey().export_key()
            return False
        except ValueError as e:
            return True
        except Exception as e:
            raise e

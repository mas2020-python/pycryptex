"""
This module shows an example of encrypt and decrypt using RSA algorithm.
"""
import os
from pathlib import Path

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import pycryptex


def encrypt_data(clear_data: bytes, public_key: str) -> list:
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
    # data = "I met aliens in UFO. Here is the map.".encode("utf-8")
    # file_out = open("encrypted_data.bin", "wb")
    encbytes_out = list()
    recipient_key = RSA.import_key(open(public_key).read())
    session_key = get_random_bytes(32)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(clear_data)
    # for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext):
    #     print(f"x: {x}\n")
    for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext):
        encbytes_out.append(x)
    return encbytes_out


def encrypt_file(file: str, public_key: str, remove=False):
    """
    Encrypt the file and create a new file appending .enc.

    :param file: file to encrypt
    :param public_key: RSA key used for encryption
    :param remove: bool to specify if remove original file
    :return: None
    """
    with open(file, 'rb') as byte_reader:
        # Read all bytes
        clear_bytes = byte_reader.read(-1)
    enc_bytes_list = encrypt_data(clear_bytes, public_key)
    with open("".join((file, ".enc")), "wb") as f:
        for b in enc_bytes_list:
            f.write(b)
    if remove:
        os.remove(file)


def decrypt_file(file: str, private_key: str, remove=False, passprhase=None):
    """
    Decrypt the file passed as argument and create a new file removing the .enc extension.

    :param file: encrypted file to decrypt
    :param private_key: RSA private key used for decryption
    :param remove: bool to specify if remove the encrypted file
    :return: the name of the file that has been decrypted
    """
    with open(file, 'rb') as byte_reader:
        # Read all bytes
        enc_bytes = byte_reader.read(-1)
    clear_bytes_list = decrypt_data(enc_bytes, private_key, passprhase)
    with open(file[:-4], "wb") as f:
        f.write(clear_bytes_list)
    if remove:
        os.remove(file)
    return file[:-4]


def decrypt_data(enc_data: bytes, private_key: str, passprhase=None) -> bytes:
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
    private_key = RSA.import_key(open(private_key).read(), passphrase=passprhase)
    # get the single elements from bytes list
    enc_session_key = enc_data[:private_key.size_in_bytes()]
    nonce = enc_data[private_key.size_in_bytes():private_key.size_in_bytes() + 16]
    tag = enc_data[private_key.size_in_bytes() + 16:private_key.size_in_bytes() + 32]
    ciphertext = enc_data[private_key.size_in_bytes() + 32:]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return data


def create_keys(folder: str, passprhase=None):
    """
    Create a public key and private key pair
    :param folder: directory where to create the my_key and my_key.pub files
    :return: None
    """
    key = RSA.generate(2048)
    private_key = None
    if passprhase:
        private_key = key.export_key(passphrase=passprhase, pkcs=8,
                                     protection="scryptAndAES128-CBC")
    else:
        private_key = key.export_key()

    with open(os.path.join(folder, "my_key"), "wb") as file_out:
        file_out.write(private_key)

    public_key = key.publickey().export_key()
    with open(os.path.join(folder, "my_key.pub"), "wb") as file_out:
        file_out.write(public_key)

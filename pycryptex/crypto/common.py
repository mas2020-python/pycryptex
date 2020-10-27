"""
This module contains some common function used by the crypto modules.
"""
import os


def encrypt_file(file: str, func, remove=False, **kwargs) -> (str, bool):
    """
    Encrypt the file and create a new file appending .enc.

    :param file: file to encrypt
    :param public_key: RSA key used for encryption
    :param remove: bool to specify if remove original file
    :return: None
    """
    # if the file name ends with .enc, return ""
    if file.endswith(".pycpx"):
        return file, False
    with open(file, 'rb') as byte_reader:
        # Read all bytes
        clear_bytes = byte_reader.read(-1)
    # call the func to encrypt and convert the byte arrays into bytes to write on disk
    enc_bytes_list = func(clear_bytes, **kwargs)
    enc_filename = "".join((file, ".pycpx"))
    with open(enc_filename, "wb") as f:
        f.write(enc_bytes_list)
    if remove:
        os.remove(file)
    return enc_filename, True


def decrypt_file(file: str, func, remove=False, **kwargs) -> (str, bool):
    """
    Decrypt the file passed as argument and create a new file removing the .enc extension.

    :param file: encrypted file to decrypt
    :param private_key: RSA private key used for decryption
    :param remove: bool to specify if remove the encrypted file
    :return: the name of the file that has been decrypted
    """
    # if the file name ends with .enc, return ""
    if not file.endswith(".pycpx"):
        return file, False
    with open(file, 'rb') as byte_reader:
        # Read all bytes
        enc_bytes = byte_reader.read(-1)
    clear_bytes_list = func(enc_bytes, **kwargs)
    with open(file[:-6], "wb") as f:
        f.write(clear_bytes_list)
    if remove:
        os.remove(file)
    return file[:-6], True

import os
from click.testing import CliRunner
from Crypto.Hash import SHA256
from pycryptex.main import cli
from pycryptex.crypto.aes import AESCryptex


def test_encrypt():
    runner = CliRunner()
    if os.path.exists('encryption_area/secrets.txt.pycpx'):
        os.remove('encryption_area/secrets.txt.pycpx')
    result = runner.invoke(cli,
                           ['encrypt', '--pubkey', 'encryption_area/id_rsa.pub', 'encryption_area/secrets.txt',
                            '--keep'])
    assert result.exit_code == 0
    assert not result.exception
    assert os.path.exists('encryption_area/secrets.txt.pycpx') is True
    result = runner.invoke(cli,
                           ['encrypt', '--pubkey', 'encryption_area/id_rsa.pub', 'encryption_area/secrets.txt'])
    assert os.path.exists('encryption_area/secrets.txt.pycpx') is True
    assert os.path.exists('encryption_area/secrets.txt') is False


def test_decrypt():
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['decrypt', '--privkey', 'encryption_area/id_rsa',
                            'encryption_area/secrets.txt.pycpx'])
    assert result.exit_code == 0
    assert not result.exception
    assert os.path.exists('encryption_area/secrets.txt') is True


def test_aes():
    """
    Encryption/decryption with AES using the crypto package directly.
    :return:
    """
    aes = AESCryptex()
    arr = bytes('Python test', 'utf-8')
    enc_data = aes.encrypt_data(arr, 'test')
    dec_data = aes.decrypt_data(enc_data, 'test')
    assert b'Python test' == dec_data
    # encrypt image: calculate ori HASH -> encrypt and get enc bytes -> decrypt and get dec bytes ->
    # compare clear HASH == dec HASH
    with open('encryption_area/hawk.jpg', 'rb') as byte_reader:
        # Read all bytes
        clear_bytes = byte_reader.read(-1)
    ori_hash_object = SHA256.new(data=clear_bytes)

    # encrypt image
    enc_data = aes.encrypt_data(clear_bytes, 'test')  # get encrypted data bytes
    dec_data = aes.decrypt_data(enc_data, 'test')  # get decrypted data bytes
    dec_hash_object = SHA256.new(data=dec_data)
    # compare ori HASH and dec HASH
    assert ori_hash_object.hexdigest() == dec_hash_object.hexdigest()

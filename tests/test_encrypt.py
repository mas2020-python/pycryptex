import os
from click.testing import CliRunner
from pycryptex.main import cli


def test_encrypt():
    runner = CliRunner()
    if os.path.exists('test/secrets.txt.enc'):
        os.remove('test/secrets.txt.enc')
    result = runner.invoke(cli,
                           ['encrypt', '--pubkey', 'test/id_rsa.pub', 'test/secrets.txt', '--keep'])
    assert result.exit_code == 0
    assert not result.exception
    assert os.path.exists('test/secrets.txt.enc') is True
    result = runner.invoke(cli,
                           ['encrypt', '--pubkey', 'test/id_rsa.pub', 'test/secrets.txt'])
    assert os.path.exists('test/secrets.txt.enc') is True
    assert os.path.exists('test/secrets.txt') is False


def test_decrypt():
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['decrypt', '--privkey', 'test/id_rsa',
                            'test/secrets.txt.enc'])
    assert result.exit_code == 0
    assert not result.exception
    assert os.path.exists('test/secrets.txt') is True

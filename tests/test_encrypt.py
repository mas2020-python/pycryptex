from click.testing import CliRunner
from pycryptex.main import cli


def test_encrypt():
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--verbose', 'encrypt', '--pubkey', 'keys/my_key.pub','test/appway.png'])
    assert result.exit_code == 0
    print(result.exit_code)
    assert not result.exception

def test_decrypt():
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['decrypt', '--privkey', '/Users/andrea.genovesi/.ssh/keys/id_rsa',
                            '/Users/andrea.genovesi/ganttproject.log.enc'])
    assert result.exit_code == 0
    print(result.exit_code)
    assert not result.exception

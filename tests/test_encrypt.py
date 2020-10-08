from click.testing import CliRunner
from pycryptex.main import cli


def test_encrypt():
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--verbose', 'encrypt', '--pubkey', 'keys/my_key.pub','test/appway.png'])
    assert result.exit_code == 0
    print(result.exit_code)
    assert not result.exception

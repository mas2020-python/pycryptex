import os
from pathlib import Path
from click.testing import CliRunner
from pycryptex.main import cli


def test_create_config():
    runner = CliRunner()
    pycryptex_config_file = os.path.join(Path.home(), '.pycryptex', 'pycryptex.toml')
    pycryptex_exists = os.path.exists(pycryptex_config_file)
    result = runner.invoke(cli,
                           ['create-config'])
    assert result.exit_code == 0
    assert not result.exception
    if not pycryptex_exists:
        assert os.path.exists(pycryptex_config_file) is True
    else:
        assert os.path.exists(pycryptex_config_file) is True

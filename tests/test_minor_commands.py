import os
import pytest
from pathlib import Path
from click.testing import CliRunner
from pycryptex.main import cli
from pycryptex.internal.utils import read_config


def test_create_config():
    runner = CliRunner()
    pycryptex_config_file = os.path.join(Path.home(), '.pycryptex', 'pycryptex.toml')
    if os.path.exists(pycryptex_config_file):
        os.remove(pycryptex_config_file)
    result = runner.invoke(cli,
                           ['create-config'])
    assert result.exit_code == 0
    assert not result.exception
    assert os.path.exists(pycryptex_config_file) is True
    try:
        read_config()
    except Exception as e:
        pytest.fail(f"read_config raises an Exception, test FAILED {e}")

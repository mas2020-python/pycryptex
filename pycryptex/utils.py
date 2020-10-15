"""
Utils module for repetitive jobs.
"""
import os
import sys
from pathlib import Path
import pycryptex
from os import path
import toml
import click


def get_home() -> str:
    return str(Path.home())


def create_home_folder():
    """
    If it does not exist $HOME/.pycryptex folder will be created
    :return:
    """
    pycryptex_folder = os.path.join(get_home(), '.pycryptex')
    if not os.path.exists(pycryptex_folder):
        os.mkdir(pycryptex_folder)
        return True, pycryptex_folder
    return False, pycryptex_folder


def create_config() -> bool:
    """
    If it does not exist $HOME/.pycryptex/pycryptex.toml file will be created
    :return:
    """
    # first check to create $HOME/.pycryptex folder
    create_home_folder()
    pycryptex_config_file = os.path.join(get_home(), '.pycryptex', 'pycryptex.toml')

    if not os.path.exists(pycryptex_config_file):
        with open(pycryptex_config_file, "w") as f:
            f.write("""---
# Configuration file for pycryptex
[config]
# path to the pager application where to see decrypted file
pager = "vim"
# number of seconds the application will delete a file decrypted passing the -s option flag
wait_delete_time = 0""")
            return True
    return False


def read_config():
    try:
        config_path = os.path.join(get_home(), '.pycryptex', 'pycryptex.toml')
        if path.exists(config_path):
            pycryptex.config_file = toml.load(config_path)
        else:
            pycryptex.config_file = {
                "config": {
                    'pager': 'vim',
                    'wait_delete_time': 0
                }
            }
    except Exception as e:
        click.echo(click.style(f"Houston, we have a problem in read_config: {e}", fg="red", bold=True))
        sys.exit(1)

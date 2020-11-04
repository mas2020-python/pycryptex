"""
Utils module for repetitive jobs.
"""
import os
from pathlib import Path
import subprocess
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
            f.write("""# Configuration file for pycryptex
[config]
# path to the pager application where to see decrypted file. Other pager could be 'code -', 'sublime -', 'nano -'
# from version 2.2, 'cat' (not suggested as stays output into the shell), 'vim -'...
pager = "less"
# default private key for RSA decryption
private-key = ""
# default public key for RSA encryption
public-key = ""
""")
            return True
    return False


def read_config():
    config_path = os.path.join(get_home(), '.pycryptex', 'pycryptex.toml')
    if path.exists(config_path):
        pycryptex.config_file = toml.load(config_path)
    else:
        pycryptex.config_file = {
            "config": {
                'pager': 'vim',
                'private-key': "",
                'public-key': "",
            }
        }


def show_config():
    """
    Show the config file content if the file is present.
    :return:
    """
    config_path = os.path.join(get_home(), '.pycryptex', 'pycryptex.toml')
    if path.exists(config_path):
        with open(config_path, 'r') as reader:
            # Read all bytes
            click.echo(click.style(reader.read(), fg="magenta", bold=False))
            click.echo(f"PyCryptex config file is read from here: {config_path}")
    else:
        click.echo(
            click.style(f"● Nothing to do, file pycryptex.toml has not been created yet...", fg="white", bold=False))


def get_incomplete_searches(incomplete: str) -> (str, str):
    # if incomplete is a dir, return current_dir = incomplete, init_word = ""
    if os.path.isdir(incomplete):
        return incomplete, ""

    # if incomplete is NOT a dir, join with os.getcwd(), if ok incomplete = current + incomplete, init_word = ""
    if os.path.isdir(os.path.join(Path(os.getcwd()), incomplete)):
        return os.path.join(Path(os.getcwd()), incomplete), ""

    # if incomplete contains / remove the last word previous the last slash, join it with os.getcwd():
    if incomplete.find("/") > -1:
        s = incomplete.split('/')
        dir = "/".join(s[: -1])
        if os.path.isdir(dir):
            return dir, s[-1]
    # return current dir, initial_word == incomplete
    return os.getcwd(), incomplete


def open_pager(config, dec_bytes: bytes):
    # load config file first
    read_config()
    if config.verbose:
        click.echo(click.style(f"config_file loaded: {pycryptex.config_file}", fg="magenta", bold=True))
    process = subprocess.Popen(pycryptex.config_file['config']['pager'].split(' '), shell=False, stdin=subprocess.PIPE)
    process.communicate(dec_bytes)


def count_file(path, no_nested: bool) -> int:
    """
    Count the file in a folder and its nested folders
    :param path: directory where begins to count
    :return: total files number
    """
    i = 0
    if no_nested:
        currentDirectory = Path(path)
        for currentFile in currentDirectory.iterdir():
            if currentFile.is_file():
                i += 1
        return i
    else:
        for root, d_names, f_names in os.walk(path):
            for f in f_names:
                i += 1
        return i


def is_valid_path(path) -> bool:
    # test first for file existence
    if not os.path.exists(path):
        click.echo(click.style(f"● Nothing to do, file or folder {path} doesn't exist!", fg="white", bold=False))
        return False
    return True

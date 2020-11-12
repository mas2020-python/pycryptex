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


def create_config(force: bool) -> bool:
    """
    If it does not exist $HOME/.pycryptex/pycryptex.toml file will be created
    :return:
    """
    # first check to create $HOME/.pycryptex folder
    create_home_folder()
    pycryptex_config_file = os.path.join(get_home(), '.pycryptex', 'pycryptex.toml')

    if not os.path.exists(pycryptex_config_file) or force:
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
# (default false) true/false to secure delete files (if activated deletion of files becomes slower)
secure-deletion = false
# number of passes for secure deletion. Means how many times PyCryptex write random data into the file.
# greater is the number you adopt major security but deletion becomes slower
secure-deletion-passes = 1
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
                'secure-deletion': False,
                'secure-deletion-passes': 1,
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


def secure_delete(path, passes=1):
    """
    Secure remove file, thanks to:
    https://stackoverflow.com/users/2868788/phealy3330
    to comment this article:
    https://stackoverflow.com/questions/17455300/python-securely-remove-file
    :param path: path to remove
    :param passes: (default 1) number of passes
    :return:
    """
    if not os.path.isfile(path):
        raise Exception(f"{path} is not a valid file, cannot securely delete!")

    with open(path, "ba+", buffering=0) as delfile:
        length = delfile.tell()
    delfile.close()
    with open(path, "br+", buffering=0) as delfile:
        for i in range(passes):
            delfile.seek(0, 0)
            delfile.write(os.urandom(length))
        delfile.seek(0)
        for x in range(length):
            delfile.write(b'\x00')
    # file deletion
    os.remove(path)

    if pycryptex.config_params.verbose:
        click.echo(click.style(f"secure deletion of {path} with {passes} passes", fg="magenta", bold=False))
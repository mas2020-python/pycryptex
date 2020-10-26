import os
from pathlib import Path
import sys
from getpass import getpass
from pycryptex.crypto.rsa import RSACryptex
import pycryptex
from os import path
import click
from tqdm import tqdm
from pycryptex import utils
from pycryptex.utils import timer
from pycryptex.crypto import common
from pycryptex.crypto.aes import AESCryptex


class Config():
    """
    This class is to pass some configuration trough the commands
    """

    def __init__(self):
        pass


# Decorator that will create a new instance of Config class. The instance is config and the object can be passed
# through the commands
pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.version_option(version=None, message="pycryptex CLI application (version: %(version)s)")
@click.option('--verbose', "-v", is_flag=True, help='bool, to specify if needed a verbose mode')
@pass_config
def cli(config, verbose):
    """
    This command is executed before other commands in the same group. The group commands
    are between the main command (pycrypto) and the single commands.

    For instance:
    pycryptex --verbose encrypt test/appway.png

    Using config.verbose is possible to pass verbose from a command to another
    """
    config.verbose = verbose


@cli.command()
@click.argument('file', required=True)
@click.option('--pubkey', default="", help='(optional) specify the RSA public key')
@click.option('--keep', '-k', is_flag=True, default=False,
              help="(optional, bool=False) if True, do not remove the original file")
@click.option('--no-nested', is_flag=True, default=False,
              help="(optional, bool=False) in case FILE is a folder, pass it to avoid encrypting the nested folders")
@pass_config
def encrypt(config, file, pubkey, keep, no_nested):
    """Encrypt files or folders using RSA/AES algorithms"""
    try:
        # in case of pubkey is not passed, pycryptex calculates the default path
        if len(pubkey) == 0:
            pubkey = os.path.join(utils.get_home(), '.pycryptex', "my_key.pub")
        # check if the key exists
        if not path.exists(pubkey):
            echo_invalid_key_msg(pubkey, "pubkey")
            return
        rsa: RSACryptex = RSACryptex()
        # check if the file param is a file or a dir
        if os.path.isdir(file):
            encrypt_decrypt_folder(rsa.encrypt_data, True, folder=file, keep=keep, no_nested=no_nested,
                                   public_key=pubkey)
            click.echo(click.style(f"👍 Folder encrypted successfully!", fg="green", bold=True))
        else:
            # encryption of the file
            f, done = common.encrypt_file(file=file, func=rsa.encrypt_data, remove=not keep, public_key=pubkey)
            if done:
                click.echo(click.style(f"👍 File encrypted successfully in {f}", fg="green", bold=True))
            else:
                click.echo(click.style(f"👍 Nothing to do, file already encrypted!", fg="yellow", bold=False))

        if config.verbose:
            click.echo(click.style(f"pubkey used is: {pubkey}", fg="magenta", bold=False))
            click.echo(click.style(f"config_file loaded: {pycryptex.config_file}", fg="magenta", bold=True))
    except Exception as e:
        click.echo(click.style(f"● Houston, help: {e}, {type(e)}", fg="red", bold=True))
        sys.exit(2)


@cli.command()
@click.argument('file', required=True)
@click.option('--privkey', default="", help='(optional) specify the RSA private key')
@click.option('--keep', '-k', is_flag=True, default=False,
              help="(optional, bool=False) if True, do not remove the original file")
@click.option('--pager', '-p', is_flag=True,
              help="(optional, bool=False) open the pager to read decrypted file (only if the FILE arg is a file)")
@click.option('--no-nested', is_flag=True, default=False,
              help="(optional, bool=False) in case FILE is a folder, pass it to avoid decrypting the nested folders")
@pass_config
def decrypt(config, file, privkey, keep, pager, no_nested):
    """Decrypt files or folders using RSA/AES algorithms"""
    try:
        f = ""
        # in case of pubkey is not passed, pycryptex calculates the default path
        if len(privkey) == 0:
            privkey = os.path.join(utils.get_home(), '.pycryptex', 'my_key')
        if config.verbose:
            click.echo(click.style(f"priv_key used is: {privkey}", fg="magenta", bold=False))
            # check if the key exists
        if not path.exists(privkey):
            echo_invalid_key_msg(privkey, "privkey")
            return

        # check if the private key has a password
        passphrase = None
        if RSACryptex.is_privatekey_protected(privkey):
            passphrase = getpass("Please insert your passphrase: ")
        rsa: RSACryptex = RSACryptex()
        if os.path.isdir(file):
            encrypt_decrypt_folder(rsa.decrypt_data, False, folder=file, keep=keep,
                                   no_nested=no_nested, passprhase=passphrase, private_key=privkey)
            click.echo(click.style(f"👍 Folder decrypted successfully!", fg="green", bold=True))
        else:  # single file case
            f, done = common.decrypt_file(file=file, func=rsa.decrypt_data, remove=not keep, passprhase=passphrase,
                                          private_key=privkey)
            if done:
                click.echo(click.style(f"👍 File decrypted successfully in {f}!", fg="green", bold=True))
            else:
                click.echo(click.style(f"👍 Nothing to do, file already decrypted!", fg="yellow", bold=False))
            # open file in a pager
            if pager:
                utils.open_pager(config, f)

    except ValueError as e:
        click.echo(click.style(f"Houston, help: it is possible that you use the wrong key file to decrypt "
                               f"the document or that the passphrase is incorrect. \nTry with the private key "
                               f"corresponding to the public key used to encrypt the file: {e}", fg="red", bold=True))
        sys.exit(2)
    except Exception as e:
        click.echo(click.style(f"● Houston, help: {e}, {type(e)}", fg="red", bold=True))
        sys.exit(2)


@cli.command()
@pass_config
def create_keys(config):
    """
    Create RSA public/private keys pair into the
    '$HOME/.pycryptex' folder.
    """
    try:
        # does keys exist in the target folder?
        is_created, pycryptex_folder = utils.create_home_folder()
        if is_created:
            click.echo(click.style(f"👍 .pycryptex folder created in: {pycryptex_folder}", fg="green", bold=False))
        if os.path.exists(os.path.join(pycryptex_folder, 'my_key')) or \
                os.path.exists(os.path.join(pycryptex_folder, 'my_key.pub')):
            click.echo(click.style(
                "[PAY ATTENTION]\n"
                "The standard keys are present into the default .pycryptex folder. If you confirm to proceed and\n"
                "you already have some document encrypted, you will not be able to open them (if you haven't also copied\n"
                "keys in another location!)", fg="red", bold=True))

        answer = input(f"Do you confirm keys creation into {pycryptex_folder}? (y/n) ")
        if answer in ('y', 'yes'):
            answer = input(f"To make your password more secure, do you like to add a passprhase? (y/n) ")
            passprhase = None
            if answer in ('y', 'yes'):
                passprhase = getpass("Please insert your passprhase: ")
                passprhase2 = getpass("Please confirm your passprhase: ")
                if passprhase != passprhase2:
                    raise Exception('passwords doesn\'t match!')
            # creation of the keys
            RSACryptex.create_keys(pycryptex_folder, passprhase)
            click.echo(
                click.style("New keys created successfully! Now you can use the other commands, happy encryption!",
                            fg="green", bold=True))
        else:
            click.echo("Keys creation aborted by the user")
    except Exception as e:
        click.echo(
            click.style(f"● Houston, we have a problem during the creation of the keys: {e}", fg="red", bold=True))
        sys.exit(2)


@cli.command()
@pass_config
def create_config(config):
    """
    Create the config file in the $HOME/.pycryptex folder if the file doesn't exist
    """
    try:
        if utils.create_config():
            click.echo(click.style(f"👍 pycryptex.toml file created in: "
                                   f"{os.path.join(utils.get_home(), '.pycryptex', 'pycryptex.toml')}", fg="green",
                                   bold=False))
        else:
            click.echo(click.style(f"👍 nothing to do, file "
                                   f"{os.path.join(utils.get_home(), '.pycryptex', 'pycryptex.toml')} already exists!",
                                   fg="magenta", bold=False))
    except Exception as e:
        click.echo(click.style(f"● Houston, help: {e}", fg="red", bold=True))
        sys.exit(2)


@cli.command()
@click.argument('file', required=True)
@click.option('--keep', '-k', is_flag=True, default=False,
              help="(optional, bool=False) if True, do not remove the original file")
@click.option('--no-nested', is_flag=True, default=False,
              help="(optional, bool=False) in case FILE is a folder, pass it to avoid encrypting the nested folders")
@pass_config
def encrypt_aes(config, file, keep, no_nested):
    """Encrypt files or folders using AES encryption"""
    try:
        encrypt_decrypt_aes(config, file, keep, no_nested, True)
    except Exception as e:
        click.echo(click.style(f"● Houston, help: {e}, {type(e)}", fg="red", bold=True))
        sys.exit(2)


@cli.command()
@click.argument('file', required=True)
@click.option('--keep', '-k', is_flag=True, default=False,
              help="(optional, bool=False) if True, do not remove the original file")
@click.option('--no-nested', is_flag=True, default=False,
              help="(optional, bool=False) in case FILE is a folder, pass it to avoid encrypting the nested folders")
@pass_config
def decrypt_aes(config, file, keep, no_nested):
    """Decrypt files or folders using AES encryption"""
    try:
        encrypt_decrypt_aes(config, file, keep, no_nested, False)
    except ValueError as e:
        click.echo(click.style(f"Houston, help: it is possible that the password you used is incorrect! [{e}]",
                               fg="red", bold=True))
        sys.exit(2)
    except Exception as e:
        click.echo(click.style(f"● Houston, help: {e}, {type(e)}", fg="red", bold=True))
        sys.exit(2)


def echo_invalid_key_msg(missing_path: str, key_name: str):
    click.echo(
        click.style(f"Houston, help: the key is missing in '{missing_path}'", fg="red", bold=False))
    click.echo(f"If you have your own key, pass the --{key_name} argument or, if you need pycryptex create "
               "the keys for you, type:\n"
               "pycryptex create-keys")


@timer
def encrypt_decrypt_folder(func, is_encrypt: bool, folder: str, keep: bool, no_nested: bool = False, **kwargs):
    """
    Function to encrypt or decrypt a folder.
    :param is_encrypt:
    :param folder: folder path
    :param key:
    :param keep:
    :param passprhase:
    :return:
    """
    click.echo(click.style(f"● Collecting folder files...", fg="magenta", bold=True))
    total = utils.count_file(folder, no_nested)
    click.echo(click.style(f"Number of files read in {folder} are: {total}", fg="white", bold=True))
    with tqdm(total=total, desc='encryption state' if is_encrypt else 'decryption state') as pbar:
        # in case of no_nested uses the simple read of the first level directory, otherwise walks into all the
        # nested levels
        if no_nested:
            currentDirectory = Path(folder)
            for currentFile in currentDirectory.iterdir():
                if currentFile.is_file():
                    if is_encrypt:
                        common.encrypt_file(str(currentFile), func, remove=not keep, **kwargs)
                    else:
                        common.decrypt_file(str(currentFile), func, remove=not keep, **kwargs)
                    pbar.update(1)
        else:
            for root, dir_names, file_names in os.walk(folder):
                for f in file_names:
                    if is_encrypt:
                        common.encrypt_file(os.path.join(root, f), func, remove=not keep, **kwargs)
                    else:
                        common.decrypt_file(os.path.join(root, f), func, remove=not keep, **kwargs)
                    pbar.update(1)


def encrypt_decrypt_aes(config, file, keep, no_nested, is_encryption: bool):
    """Encrypt a file using AES encryption"""
    passprhase = getpass("Please insert your passphrase: ")
    aes = AESCryptex()
    # set var for encrytion or decryption
    crypto_func = aes.decrypt_data
    crypto_term = "decrypted"
    if is_encryption:
        crypto_term = "encrypted"
        crypto_func = aes.encrypt_data

    # check if the file param is a file or a dir
    if os.path.isdir(file):
        encrypt_decrypt_folder(crypto_func, is_encryption, folder=file, keep=keep, no_nested=no_nested,
                               pwd=passprhase)
        click.echo(click.style(f"👍 Folder {crypto_term} successfully!", fg="green", bold=True))
    else:
        # encryption/decryption of the file
        if is_encryption:
            f, done = common.encrypt_file(file, crypto_func, remove=not keep, pwd=passprhase)
        else:
            f, done = common.decrypt_file(file, crypto_func, remove=not keep, pwd=passprhase)
        if done:
            click.echo(click.style(f"👍 File {crypto_term} successfully in {f}", fg="green", bold=True))
        else:
            click.echo(click.style(f"👍 Nothing to do, file already {crypto_term}!", fg="yellow", bold=False))

    if config.verbose:
        click.echo(click.style(f"config_file loaded: {pycryptex.config_file}", fg="magenta", bold=True))


if __name__ == '__main__':
    print("main invoked!")
    cli(sys.argv[1:])

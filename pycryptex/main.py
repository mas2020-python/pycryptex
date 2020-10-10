import os
import subprocess
import sys
from pathlib import Path
from pycryptex.crypto import rsa
import pycryptex
from os import path
import time
import click
import toml


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
    # load config file
    read_config()
    if verbose:
        click.echo(click.style(f"config_file loaded: {pycryptex.config_file}", fg="magenta", bold=True))


@cli.command()
@click.argument('file', required=True)
@click.option('--pubkey', default="my_key.pub", help='(optional) specify the RSA public key')
@click.option('--remove', '-r', is_flag=True, help="(optional, bool=False) to indicate if remove or not the file")
@pass_config
def encrypt(config, file, pubkey, remove):
    """Encrypt a file"""
    try:
        # in case of pubkey is not passed, pycryptex calculates the default path
        if pubkey == "my_key.pub":
            pubkey = os.path.join(get_home(), '.pycryptex', pubkey)
        # check if pubkey exists
        if not path.exists(pubkey):
            click.echo(
                click.style(f"Houston, we have a problem: the pubkey is missing in '{pubkey}'", fg="red", bold=False))
            click.echo("If you have your own key, pass the --pubkey argument or, if you need pycryptex create "
                       "the keys for you, type:\n"
                       "pycryptex create-keys")
            return
        # encryption of the file
        rsa.encrypt_file(file=file, public_key=pubkey, remove=remove)
        if config.verbose:
            click.echo(click.style(f"pubkey used is: {pubkey}", fg="magenta", bold=False))
        click.echo(click.style("File encrypted successfully!", fg="green", bold=True))
    except Exception as e:
        click.echo(click.style(f"Houston, we have a problem: {e}, {type(e)}", fg="red", bold=True))
        sys.exit(2)


@cli.command()
@click.argument('file', required=True)
@click.option('--privkey', default="my_key", help='(optional) specify the RSA private key')
@click.option('--remove', '-r', is_flag=True, help="(optional, bool=False) passing this option the encrypted file will"
                                                   "be removed")
@click.option('-s', is_flag=True, help="(optional, bool=False) passing this option the decrypted file will"
                                       "be removed")
@click.option('--pager', '-p', is_flag=True,
              help="(optional, bool=False) to open or not the pager to read decrypted file")
@pass_config
def decrypt(config, file, privkey, remove, s, pager):
    """Decrypt a file"""
    try:
        # in case of pubkey is not passed, pycryptex calculates the default path
        if privkey == "my_key":
            privkey = os.path.join(get_home(), '.pycryptex', privkey)
            try:
                f = rsa.decrypt_file(file=file, private_key=privkey, remove=remove)
            except ValueError as e:
                # try again to decrypt passing the passprhase
                passprhase = input("Please insert your passprhase: ")
                f = rsa.decrypt_file(file=file, private_key=privkey, remove=remove, passprhase=passprhase)

        # open file in a pager
        if pager:
            exit_code = subprocess.call([pycryptex.config_file['config']['pager'], f])
            if exit_code == 0:
                # if True delete the decrypted file
                time.sleep(pycryptex.config_file['config']['wait_delete_time'])
                if s:
                    os.remove(f)
            else:
                click.echo(click.style(f"Houston, we have a problem: the opened subprocess has a return value equal to"
                                       f" {exit_code}", fg="red", bold=True))
        if config.verbose:
            click.echo(click.style(f"priv_key used is: {privkey}", fg="magenta", bold=False))
        click.echo(click.style("File decrypted successfully!", fg="green", bold=True))
    except ValueError as e:
        click.echo(click.style(f"Houston, we have a problem: it is possible that you use the wrong key file to decrypt "
                               f"the document or that the passprhase is incorrect. \nTry with the private key "
                               f"corresponding to the public key used to encrypt the file.", fg="red", bold=True))
        sys.exit(2)
    except Exception as e:
        click.echo(click.style(f"Houston, we have a problem: {e}, {type(e)}", fg="red", bold=True))
        sys.exit(2)


@cli.command()
@pass_config
def create_keys(config):
    """
    Create a public and private key pair into the
    '$HOME/.pycryptex' folder.
    """
    try:
        # does keys exist in the target folder?
        home = Path.home()
        pycryptex_folder = os.path.join(home, '.pycryptex')
        if os.path.exists(os.path.join(pycryptex_folder, 'my_key')) or \
                os.path.exists(os.path.join(pycryptex_folder, 'my_key.pub')):
            click.echo(click.style(
                "[PAY ATTENTION]\n"
                "The standard keys are present into the default .pycryptex folder. If you confirm to proceed and\n"
                "you already have some document encrypted, you will not be able to open them (if you haven't copied\n"
                "keys in another location!", fg="red", bold=True))

        answer = input(f"Do you confirm keys creation into {pycryptex_folder}? (y/n)")
        if answer in ('y', 'yes'):
            answer = input(f"To robust your key, do you need to add a passprhase? (y/n)")
            passprhase = None
            if answer in ('y', 'yes'):
                passprhase = input("Please insert your passprhase: ")
            # creation of the keys
            rsa.create_keys(pycryptex_folder, passprhase)
            click.echo(
                click.style("New keys created successfully! Now you can use the other commands, happy encryption!",
                            fg="green", bold=True))
        else:
            click.echo("Keys creation aborted by the user")
    except Exception as e:
        click.echo(click.style(f"Houston, we have a problem during the creation of the keys: {e}", fg="red", bold=True))
        sys.exit(2)


def get_home() -> str:
    return str(Path.home())


def read_config():
    try:
        config_path = os.path.join(get_home(), '.pycryptex', 'pycryptex.toml')
        if path.exists(config_path):
            pycryptex.config_file = toml.load(config_path)
        else:
            pycryptex.config_file = {
                "config": {
                    'pager': 'vim'
                }
            }
    except Exception as e:
        click.echo(click.style(f"Houston, we have a problem in read_config: {e}", fg="red", bold=True))
        sys.exit(1)

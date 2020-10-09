import setuptools
from setuptools import setup
import os
from pathlib import Path


def _post_install():
    """
    Post installation steps are:
    - create $HOME/.cryptex folder and $HOME/.cryptex/tmp
    - create a default version of pycryptex.toml
    :return:
    """
    # .pycryptex folder creation
    home = Path.home()
    pycryptex_folder = os.path.join(home, '.pycryptex')
    if not os.path.exists(pycryptex_folder):
        os.mkdir(pycryptex_folder)
        # print(f"Hi, pycryptex has created for you the .pycryptex folder in {pycryptex_folder}")

    # .pycryptex/tmp folder creation
    pycryptex_tmp_folder = os.path.join(home, '.pycryptex', 'tmp')
    if not os.path.exists(pycryptex_tmp_folder):
        os.mkdir(pycryptex_tmp_folder)

    # create a default version of pycryptex.toml
    pycryptex_config_file = os.path.join(home, '.pycryptex', 'pycryptex.toml')
    if not os.path.exists(pycryptex_config_file):
        with open(pycryptex_config_file, "w") as f:
            f.write("""# Configuration file for pycryptex
[config]
# path to the pager application where to see decrypted file
pager = "vim"
# number of seconds the application will delete a file decrypted passing the s option flag
wait_delete_time = 2
            """)
            # print(f"Hi, pycryptex has created for you the default config file {pycryptex_config_file}")


setup(
    name="pycryptex",
    version="0.2.0-dev",
    # package_dir={'': 'pycryptex'},
    packages=setuptools.find_packages(),
    install_requires=[
        'CLick',
        'pycryptodome',
    ],
    entry_points='''
        [console_scripts]
        pycryptex=pycryptex.main:cli
    ''',
)

_post_install()

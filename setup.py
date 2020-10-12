import setuptools
from setuptools import setup
import os
from pathlib import Path

"""
This instruction inform setup tool to read our doc file and to include as a long description of the package.
"""
with open("README.md", "r") as fh:
    long_description = fh.read()


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
wait_delete_time = 0
            """)


setup(
    name="pycryptex",
    author="mas2020",
    author_email="andrea.genovesi@gmail.com",
    version="0.2.0",
    url="https://github.com/mas2020-python/pycryptex",
    description="Python CLI application to easily encrypt and decrypt file and folders. Easy and fast for the lovers"
                "of the CLI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # package_dir={'': 'pycryptex'},
    packages=setuptools.find_packages(),
    install_requires=[
        'click==7.1.2',
        'pycryptodome==3.9.8',
    ],
    entry_points='''
        [console_scripts]
        pycryptex=pycryptex.main:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

_post_install()

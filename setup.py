import setuptools
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import os


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        print("dev post install")


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        print("post install")
        os.mkdir('xxx')


setup(
    name="pycryptex",
    version="0.1.0",
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
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)

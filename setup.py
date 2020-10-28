import setuptools
from setuptools import setup
import os
from pathlib import Path

"""
This instruction inform setup tool to read our doc file and to include as a long description of the package.
"""
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pycryptex",
    author="mas2020",
    author_email="andrea.genovesi@gmail.com",
    version="0.4.0-rc1",
    url="https://github.com/mas2020-python/pycryptex",
    description="Python CLI application to easily encrypt and decrypt file and folders. Easy and fast for the lovers"
                " of the CLI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        'click==7.1.2',
        'pycryptodome==3.9.8',
        'toml==0.10.1',
        'tqdm==4.50.2',
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
    python_requires='>=3.6, <4',
)

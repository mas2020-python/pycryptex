# PyCryptex
This project is a CLI application for encryption and decryption using the pycryptodome package. For the CLI functionality it uses
Click package.


## Install application

To use `pycryptex` you need to have python3 and pip3 installed. Depending on you platform the procedure to install python can change.
Try this on your terminal:
```shell script
python3 -V
```
If you do not get an answer the best place to to start is looking into the official documentation [here](https://www.python.org/downloads/).

Then, when you have at least Python >= 3.6 and pip3 installed, simply type:
```shell script
python3 -m pip install pycryptex
```
If you are on linux you could have this warning:
```
WARNING: The script pycryptex is installed in '/home/<YOUR-HOME>/.local/bin' which is not on PATH.
```
It means that if you type `pycryptex` you get a not found error.
To solve, simply add the path to your PATH, for example, edit .bashrc in your $HOME folder as (suppose your HOME == vagrant):
```
# Add local python bin script to my PATH:
export PATH=$PATH:/home/vagrant/.local/bin
```
if you do not use BASH as a shell, search the same src file for your shell and edit in a similar way.
Then execute, in case of BASH:
```
source $HOME/.bashrc
# and then type
pycryptex
```
It should work now and for all the future updates!

### Fast start

If you want encrypt and decrypt files and folders easily and you do not want spend time to create your own encryption keys you can let
PyCryptex do the job for you (to use your own keys or understanding better the behaviour of the application refers to the rest of the documentation):
```shell script
pycryptex create-keys
``` 
answer 'yes' and decide if protect the private key with a password (it's your security choice).
PyCryptex will create the standard key in your *$HOME/.pycryptex* folder.

***IMPORTANT***: you will use your public key (my_key.pub) for encrypt and you private key (my_key) for decrypt. Do not leave the keys in the same place, secure you private key as best as you can, as you do with your private HOME keys ;-)!

At this point you can simply encrypt a file or a folder using:
```shell script
pycryptex encrypt <FILE-OR-FOLDER>
```
everytime you need to know the options behind a command digit:
```shell script
pycryptex <command> --help
```
To decrypt a file or a folder type:
```shell script
pycryptex decrypt <FILE-OR-FOLDER>
```
That's it for the PyCryptex in a `nutshell`. Go ahead with the lecture to figure out how to make the most of the application.

***Happy Encryption!!!***

### Using application

You can get help with:
````shell script
pycryptex --help
````

PyCryptex encryption works with symmetric or asymmetric algorithms based on the arguments passed.
To the standard encryption/decryption ``pycryptex`` uses RSA keys pair. In particular, it encrypts using the public key of the user and decrypts
using the private key. For better performance ``pycryptex`` behind the scene uses for encryption and decryption the AES algorithm.
The RSA keys are used to encrypt and decrypt the random key generated and stored as header to the file.
In this way the performance are definitely better on a large file (a 256 bit AES random key is used).


The default keys name:
- my_key: for the private key
- my_key.pub: for the public key
The folder where **`pycryptex`** searches for the key is your $HOME/.pycryptex. If you prefer to use your own
keys you can pass them directly as an argument to the encrypt and decrypt method.

### Configuration file

PyCryptex reads a configuration file located in your $HOME/.pycryptex folder named **pycryptex.toml**.
The file has the following syntax (reported are the default file):
```toml
[config]
# path to the pager application where to see decrypted file
pager = "vim"
```

### List of all commands

To an explanation of all the option of a specific command take a look directly at:
```shell script
pycryptex encrypt --help
```

Follow the list of commands:
- `encrypt`: to encrypt a single file or a folder (including sub folders).
- `decrypt`: to decrypt a single file a single file or a folder (including sub folders).
- `create-keys`: to create a public key and private key pair.
- `create-config`: to create the default config file under $HOME/.pycryptex/pycryptex.toml
- `encrypt-aes`: to encrypt a single file or a folder (including sub folders) using AES algorithm.
- `decrypt-aes`: to decrypt a single file a single file or a folder (including sub folders) using AES algorithm.

### Some examples
Some basic example usages are:
````shell script
# to encrypt passing a key
pycryptex encrypt --pubkey test/id_rsa.pub test/secrets.txt

# to encrypt using the my_key.pub in $HOME/.pycryptex folder
pycryptex encrypt test/secret.txt

# to encrypt using the my_key.pub in $HOME/.pycryptex folder maintaining the original file
pycryptex encrypt test/secret.txt --keep

# decrypt the file
pycryptex --verbose decrypt --privkey test/id_rsa test/secrets.txt.enc

# decrypt using your own private key and open the pager
pycryptex --verbose decrypt --privkey test/id_rsa -p test/secrets.txt.enc

# decrypt and open the pager (loading keys from $HOME/.pycryptex)
pycryptex decrypt -p test/secrets.txt.enc

# to create private/public key pairs
pycryptex create-keys
````

## Configuration for developers

If you want to contribute to that project, after cloning the repo type:
```shell script
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt

# (optional) to test type
python3 -m Crypto.SelfTest
```

If you need to create a new key pair you can use ssh-keygen. In such case type:
```shell script
ssh-keygen -t rsa -b 4096 -C "<your-user>@<your-domain>"
```

To install the executable package type:
````shell script
git clone https://github.com/mas2020-python/pycryptex.git
pip3 install --editable .
````

To install from PyPi test (other dependencies packages from official PyPi) type:
````shell script
pip3 install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pycryptex==<VERSION>
````

To test the application type:
```shell script
pytest
```

To deploy on PyPi test:
```shell script
python3 setup.py check
python3 setup.py bdist_wheel sdist
twine upload dist/* --repository testpypi
```
You need to have the credentials or token from the owner of the project on PyPi.
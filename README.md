# PyCryptex
This project is a CLI application for encryption and decryption using the pycryptodome package. For the CLI functionality it uses
Click package.


## Configuration for developers

If you want to contribute to that project, after cloning the repo type:
```shell script
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
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
pip3 install --editable .
````

To install from PyPi test (other dependencies packages from official PyPi) type:
````shell script
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pycryptex==<version>
````

To test the application type:
```shell script
pytest
```

To deploy on PyPi test:
```shell script
python3 setup.py bdist_wheel sdist
twine upload dist/* --repository testpypi
```
You need to have the credentials or token from the owner of the project on PyPi.

## Install application

If you like pycryptex and you want to use simply type:
```shell script
pip3 install pycryptex
```

## Using application

You can get help with:
````shell script
pycryptex --help
````

PyCryptex can encrypt using symmetric or asymmetric algorithms based on the arguments passed.
To the standard encryption/decryption ``pycryptex`` uses RSA keys pair. In particular encrypt using the public key of the user and decrypt
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
# number of seconds the application will delete a file decrypted passing the s option flag
wait_delete_time = 2
```

### List of all commands

To an explanation of all the option of a specific command take a look directly at:
```shell script
pycryptex encrypt --help
```

Follow the list of commands:
- `encrypt`: to encrypt a single file
- `decrypt`: to decrypt a single file
- `create-keys`: to create a public key and private key pair.
- `create-config`: to create the default config file under $HOME/.pycryptex/pycryptex.toml

### Some examples
Some basic example usages are:
````shell script
# to encrypt passing a key
pycryptex encrypt --pubkey test/id_rsa.pub test/secrets.txt

# to encrypt using the my_key.pub in $HOME/.pycryptex folder
pycryptex encrypt test/secret.txt

# to decrypt and delete the encrypted file
pycryptex --verbose decrypt --privkey test/id_rsa  --remove test/secrets.txt.enc

# decrypt, open the pager and then delete the decrypted file
pycryptex --verbose decrypt --privkey test/id_rsa -s -p  test/secrets.txt.enc

# decrypt, open the pager and then delete the decrypted file (loading keys from $HOME/.pycryptex)
pycryptex decrypt -sp test/secrets.txt.enc

# to create private/public key pairs
pycryptex create-keys
````
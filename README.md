# PyCryptex
This project is a CLI application for encryption and decryption using the pycryptodome package. For the CLI functionality it uses
Click package.


## Configuration for developers

If you want to contribute to that project, after cloning the repo type:
```shell script
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
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

To test the application type:
```shell script
pytest
```

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

To encrypt/decrypt some content ``pycryptex`` uses RSA keys pair. The default keys name:
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

### Some examples
Some basic example usages are:
````shell script
# to encrypt passing a key
pycryptex encrypt --pubkey keys/my_key.pub test/secret.txt

# to encrypt using the my_key.pub in $HOME/.pycryptex folder
pycryptex encrypt test/secret.txt

# to decrypt and delete the encrypted file
pycryptex --verbose decrypt --privkey keys/my_key  --remove test/secrets.txt.enc

# decrypt, open the pager and then delete the decrypted file
pycryptex --verbose decrypt --privkey keys/my_key  -s -p  test/secrets.txt.enc

# decrypt, open the pager and then delete the decrypted file (loading keys from $HOME/.pycryptex)
pycryptex decrypt -sp test/secrets.txt.enc

# to create private and public key pair
pycryptex create-keys
````
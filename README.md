# PyCryptex

This project can be used as:

- CLI application for encryption and decryption
- a package to import in your personal project to create an encryption/decryption app

For the CLI functionality it uses `click` package and for the encryption the amazing `pycryptodome` package.

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

If you want encrypt and decrypt files and folders easily and you do not want spend time to create your own encryption keys, you can let
PyCryptex do the job for you (to use your own keys or understanding better the behaviour of the application refers to the rest of the documentation):
```shell script
pycryptex create-keys
``` 
answer 'yes' and decide if protect the private key with a password (it's your security choice).
PyCryptex will create the standard key in your *$HOME/.pycryptex* folder.

***IMPORTANT***: you will use your public key (pycryptex_key.pub) for encrypt and you private key (pycryptex_key) for decrypt. Do not leave the keys in the same place, secure you private key as best as you can, as you do with your private HOME keys ;-)!

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

#### Decryption with a pager
Pager option behaviour is changed in version `0.5.0`. Now it is possible to use `decryption` also for reading a file without saving the clear file on the system (if it is not needed).
Actually the pager is enabled only for the command `decrypt` and not for the command `decrypt-aes`.
So, for example if you decrypt without option:
```shell script
pycryptex decrypt <FILE-OR-FOLDER>
```
PyCryptex will save the decrypted file on the file system, instead if you type:
```shell script
pycryptex decrypt <FILE-OR-FOLDER> --pager
```
PyCryptex will decrypt the file in memory and redirect it on the standard input of the pager set in your configuration file.
Starting from `0.5.0` version is also changed the default pager in favour of 'less' instead of 'vim'.
You can change it to use your favourite pager (simply create the configuration file `pycryptex create-config` then edit it),
some examples are:
- `code -` to use Visual Studio Code (to enable the command `code` see the Microsoft site)
- `sublime -` to use with sublime (in case you do not have it on the executable in PATH, see on the official documentation to solve the issue)
- `vim -` to use vim
- `nano -` to use nano (starting from version 2.2)

***Happy Encryption!!!***

### Using application

You can get help with:
````shell script
pycryptex --help
````

PyCryptex encryption works with symmetric or asymmetric algorithms based on the arguments passed.
To the standard encryption/decryption ``pycryptex`` uses RSA keys pair. In particular, it encrypts using the public key of the user and decrypts
using the private key. For better performance ``pycryptex`` behind the scene uses the AES algorithm.
The RSA keys are used to encrypt and decrypt the random key generated and stored as header to the file.
In this way the performance are definitely better on a large file (a 256 bit AES random key is used).


The default keys name:
- pycryptex_key: for the private key
- pycryptex_key.pub: for the public key
The folder where **`pycryptex`** searches for the key is your $HOME/.pycryptex. If you prefer to use your own
keys you can pass them directly as an argument to the encrypt and decrypt method.

An alternative, starting from version 0.4.0, could be save the path of the keys in the pycryptex confi file.

**PyCryptex determines the RSA keys to use** for the `encrypt` and `decrypt` methods, follow these rules:

- if the option --privkey or --pubkey is specified, it loads the corresponding file
- if no option key is specified:
    - if is present privkey or pubkey field in *$HOME/.pycryptex/pycryptex.toml* it loads the corresponding file
    - loads pycryptex_key as private key and pycryptex_key.pub located in *$HOME/.pycryptex* directory
 
These rules are not valid when you use `encrypt-aes` and `decrypt-aes` commands that always ask for a console password.

### Configuration file

PyCryptex reads a configuration file located in your $HOME/.pycryptex folder named **pycryptex.toml**.
The file has the following syntax (reported are the default file):
```toml
[config]
# path to the pager application where to see decrypted file
pager = "vim"
# default private key for RSA decryption
private-key = ""
# default public key for RSA encryption
public-key = ""
# (default false) true/false to secure delete files (if activated deletion of files becomes slower)
secure-deletion = false
# number of passes for secure deletion. Means how many times PyCryptex write random data into the file.
# greater is the number you adopt, major security you introduce but deletion becomes slower.
secure-deletion-passes = 1
```

#### Secure file deletion
Starting from `0.5.0` it is possible to set the config key `secure-deletion` = true. Doing this, the clear file/s, 
after the encryption, will be removed safely. It's possible to configure how many passes to run to mix up the file content
before deleting it.

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
- `show-config`: to show the configuration file if present into the $HOME/.pycryptex folder
- `encrypt-aes`: to encrypt a single file or a folder (including sub folders) using AES algorithm.
- `decrypt-aes`: to decrypt a single file a single file or a folder (including sub folders) using AES algorithm.

### Some examples
Some basic example usages are:
````shell script
# to encrypt passing a key
pycryptex encrypt --pubkey test/id_rsa.pub test/secrets.txt

# to encrypt using the pycryptex_key.pub in $HOME/.pycryptex folder
pycryptex encrypt test/secret.txt

# to encrypt using the pycryptex_key.pub in $HOME/.pycryptex folder maintaining the original file
pycryptex encrypt test/secret.txt --keep

# decrypt the file
pycryptex --verbose decrypt --privkey test/id_rsa test/secrets.txt.pycpx

# decrypt using your own private key and open the pager
pycryptex --verbose decrypt --privkey test/id_rsa -p test/secrets.txt.pycpx

# decrypt and open the pager (loading keys from $HOME/.pycryptex)
pycryptex decrypt -p test/secrets.txt.pycpx

# to create private/public key pairs
pycryptex create-keys
````
To combine decrypt + read and modify a file + encrypt again you can use something as:
```shell script
pycryptex decrypt --privkey <YOUR-PATH-TO-PRIVATE-KEY> <FILE.pycypx> \
&& vim <FILE> && \
pycryptex encrypt --pubkey <YOUR-PATH-TO-PUBLIC-KEY> <FILE>
```
By this way, you can change the clear content also using the right pager, as vim for example.
In case your keys are in your `pycryptex` HOME folder or set into the `pycryptex.toml` file, you can omit to pass them.
If you need only read an encrypted file content use simple the --pager option as described before.

### Shell auto completion for pycryptex
PyCryptex commands, options and arguments can be added to your favourite shell for the auto completion.
After you have installed the application follow the instructions choosing the shell you have.

#### `bash` configuration
If your favourite shell is **`bash`** then type:
```shell script
cd <YOUR-FOLDER>
# type this command
_PYCRYPTEX_COMPLETE=source_bash pycryptex > pycryptex.sh
```
now you that have the file `pycryptex.sh` open you $HOME/.bashrc file and add this content:
```shell script
vim $HOME/.bashrc
source /PATH-TO-PYCRYPTEX-SCRIPT/pycryptex.sh
```

#### `zsh` configuration
If your favourite shell is **`zsh`** then type:
```shell script
cd <YOUR-FOLDER>
# type this command
_PYCRYPTEX_COMPLETE=source_zsh pycryptex > pycryptex.sh
```
now you that have the file `pycryptex.sh` open you $HOME/.zshrc file and add this content:
```shell script
vim $HOME/.zshrc
source /PATH-TO-PYCRYPTEX-SCRIPT/pycryptex.sh
```

#### `fish` configuration
If your favourite shell is **`fish`** then type:
```shell script
_PYCRYPTEX_COMPLETE=source_fish pycryptex > ~/.config/fish/completions/pycryptex-complete.fish
```

## Configuration for developers

If you want to contribute to that project, after cloning the repo type:
```shell script
git clone https://github.com/mas2020-python/pycryptex.git
cd pycryptex
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt
python3 -m pip install pytest wheel twine

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
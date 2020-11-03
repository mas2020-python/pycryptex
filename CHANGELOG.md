# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2020-xx-xx

### Added

- 

### Fixed
- 

### Changed
- changed the behaviour option --pager for `decrypt`. Now it decrypts in memory and open the pager set in the configuration file. 

## [Released]

## [0.4.0] - 2020-10-30

### Added

- private and public key path in the pycryptex config file to set you default keys at the path you prefer
- `aes-encrypt` and `aes-decrypt` as new commands to encrypt/decrypt using AES algorithm
- feature to encrypt/decrypt folder and subfolders with RSA or AES

### Fixed
- remove wait_delete_time from config file and README file

### Changed
- name of the default PyCryptex keys in pycryptex_key and pycryptex_key.pub
- added the --keep option as a default for encryption/decryption. Removed the --remove option
- improvement to decrypt function

## [0.3.0] - 2020-10-21

### Added

- added new command `create-config` to create a template of the pycrytex.toml
- mask text on user input when a password is requested to decrypt a RSA private key

### Fixed
- during the reading of auto generated pycryptex.toml file
- issue when decrypting a file without having the default private key

## [0.2.0] - 2020-10-12

### Added

- added `create-keys` command to create a new private/public key pair

### Fixed
- masked text on the user input when a password is requested

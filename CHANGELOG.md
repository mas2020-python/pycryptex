# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Released]

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

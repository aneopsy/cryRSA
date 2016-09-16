# CryRSA -  RSA Encryption & Decryption tool

CryRSA est un outil en Python de chiffrage et de déchiffrage qui utilise le chiffrement RSA, compatible avec openssl.

### Prerequisities

* Python2.7
* Crypto

```
pip install Crypto
```

## Getting Started

```
$ python cryRSA.py

usage: cryRSA.py [-h] [-d] [-e] [-i INPUT] [-k KEY] [-o OUTPUT]
                 [-p PASSPHRASE] [-g GENERATE] [-V]
```

Creation des keys:

```
$ python cryRSA.py -g 4096
  Passphrase:
  Re-enter passphrase:

  Key can encrypt: True
  key can sygn: True
  key has private: True

  Public key created: public_key.pem
  Private key created: private_key.pem

```

Exemple pour chiffrer un fichier:

```
$ python crysher.py -e -k public_key.pem -i my_file -o encrypt_file
  Passphrase:
  Re-enter passphrase:
```

Chiffrer un text sur l'entrée standard (Ctrl + D: pour arreter la saissie)
```
$ python cryRSA.py -e -k public_key.pem -o encrypt_file  -p "my_password"
  hello, it's a secret message!

```

Exemple pour déchiffrer un fichier:

```
$ python crysher.py -d -key private_key.pem -i encrypt_file -o my_new_file
```

Differentes option sont disponibles:
* -p PASSPHRASE             defini un password
* -g BITS                   defini le nombre de bits de la key (1024, 4096)
* -v                        mode verbose
* -h                        affiche l'aide

## Deployment

Crysher est compatible sur:

- Linux

## Authors

* **AneoPsy** - *Initial work*

## Acknowledgments

* Cryptographie
* Python

#!/usr/bin/env python

import argparse
import os
import sys
from getpass import getpass
from itertools import combinations
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto import Random
from base64 import b64decode

VERSION = '1.1'
AUTHOR = "AneoPsy"


def generate_RSA(bits=2048, passphrase=""):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    rdm = Random.new().read
    key = RSA.generate(bits, randfunc=rdm, e=65537, progress_func=None)

    print ""
    print "Key can encrypt: " + str(key.can_encrypt())
    print "key can sygn: " + str(key.can_sign())
    print "key has private: " + str(key.has_private())
    print ""

    public_key = key.publickey().exportKey(format="PEM", passphrase=passphrase,
                                           pkcs=1)
    private_key = key.exportKey(format="PEM", passphrase=passphrase, pkcs=1)
    return private_key, public_key


def _cli_opts():
    '''
    Parse command line options.
    @returns the arguments
    '''
    mepath = unicode(os.path.abspath(sys.argv[0]))
    mebase = '%s' % (os.path.basename(mepath))
    description = '''Implements encryption/decryption RSA.'''
    desc = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog=mebase,
                                     description=description,
                                     formatter_class=desc,
                                     )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--decrypt',
                       action='store_true',
                       help='decryption mode')
    group.add_argument('-e', '--encrypt',
                       action='store_true',
                       help='encryption mode')
    parser.add_argument('-i', '--input',
                        action='store',
                        help='input file, default is stdin')
    parser.add_argument('-k', '--key',
                        action='store',
                        help='input file')
    parser.add_argument('-o', '--output',
                        action='store',
                        help='output file, default is stdout')
    parser.add_argument('-p', '--passphrase',
                        action='store',
                        help='passphrase for encrypt/decrypt operations')
    group.add_argument('-g', '--generate',
                       action='store',
                       default=1024,
                       type=int,
                       help='generate Public & Private keys')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s v' + VERSION + " by " + AUTHOR)

    args = parser.parse_args()

    if args.encrypt or args.decrypt:
        if args.key is None:
            parser.error('--encrypt and --decrypt require --key')

    return args


def _open_ios(args):
    '''
    Open the IO files.
    '''

    ifp = sys.stdin
    ofp = sys.stdout
    kfp = None

    if args.input is not None:
        try:
            ifp = open(args.input, 'r')
        except IOError:
            print 'ERROR: can\'t read file: %s' % (args.input)
            sys.exit(1)

    if args.output is not None:
        try:
            ofp = open(args.output, 'w')
        except IOError:
            print 'ERROR: can\'t write file: %s' % (args.output)
            sys.exit(1)

    if args.key is not None:
        try:
            kfp = open(args.key, 'r')
        except IOError:
            print 'ERROR: can\'t read file: %s' % (args.key)
            sys.exit(1)
    return ifp, ofp, kfp


def _close_ios(ifp, ofp, kfp):
    '''
    Close the IO files if necessary.
    '''

    if ifp != sys.stdin:
        ifp.close()

    if ofp != sys.stdout:
        ofp.close()

    if kfp != sys.stdin:
        kfp.close()


def _rundec(args):

    import ast

    ifp, ofp, kfp = _open_ios(args)
    if args.passphrase is None:
        passphrase = getpass('Passphrase: ')
    else:
        passphrase = args.passphrase

    key = RSA.importKey(kfp.read(), passphrase=passphrase)
    decrypted = key.decrypt(ast.literal_eval(str(ifp.read())))
    ofp.write(decrypted)
    _close_ios(ifp, ofp, kfp)


def _runenc(args):

    ifp, ofp, kfp = _open_ios(args)
    if args.passphrase is None:
        while True:
            passphrase = getpass('Passphrase: ')
            tmp = getpass('Re-enter passphrase: ')
            if passphrase == tmp:
                break
            print
            print 'Passphrases don\'t match, please try again.'
    else:
        passphrase = args.passphrase

    key = RSA.importKey(kfp.read(), passphrase=passphrase)
    message = ifp.read()
    out = key.encrypt(message, 32)
    ofp.write(str(out))
    _close_ios(ifp, ofp, kfp)


def _rungen(args):

    if args.passphrase is None:
        while True:
            passphrase = getpass('Passphrase: ')
            tmp = getpass('Re-enter passphrase: ')
            if passphrase == tmp:
                break
            print
            print 'Passphrases don\'t match, please try again.'
    else:
        passphrase = args.passphrase

    privateKey, publicKey = generate_RSA(args.generate, passphrase)
    try:
        f = open('public_key.pem', 'w')
        f.write(publicKey)
        f.close()
        print 'Public key created: public_key.pem'
    except IOError:
        print 'ERROR: can\'t create key.'
        sys.exit(1)
    try:
        f = open('private_key.pem', 'w')
        f.write(privateKey)
        f.close()
        print 'Private key created: private_key.pem'
    except IOError:
        print 'ERROR: can\'t create key.'
        sys.exit(1)
    exit()

if __name__ == '__main__':

    args = _cli_opts()
    if args.encrypt:
        _runenc(args)
    elif args.decrypt:
        _rundec(args)
    elif args.generate:
        _rungen(args)

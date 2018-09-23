#!/usr/bin/env python
import os
import gnupg
import sys
import getpass

#
# Script to generate gpg keys - this is a one time setup
# @author rahulsh1
# Tidbits pulled from: https://www.saltycrane.com/blog/2011/10/python-gnupg-gpg-example/
#

# Creates the GPG_Home and the public/private keys
def generate_key(email, password):
    gpg_home = os.getenv("HOME") + "/.gpghome"
    gpg = gnupg.GPG(gnupghome=gpg_home)
    input_data = gpg.gen_key_input(
        name_email=email,
        passphrase=password)
    key = gpg.gen_key(input_data)
    print(key)

    # create ascii-readable versions of public/private keys
    ascii_armored_public_keys = gpg.export_keys(key.fingerprint)
    ascii_armored_private_keys = gpg.export_keys(
        keyids=key.fingerprint,
        secret=True,
        passphrase=password,
    )

    # export the public and private keys now
    with open('keyfile.asc', 'w') as f:
        f.write(ascii_armored_public_keys)
        f.write(ascii_armored_private_keys)
    print("Wrote key file to keyfile.asc")

def main():
    args = sys.argv[1:]
    if not args:
        print("usage: " + sys.argv[0] + " <email>");
        sys.exit(1)

    email = sys.argv[1]
    passphrase = getpass.getpass()
    generate_key(email, passphrase)

if __name__ == '__main__':
    main()

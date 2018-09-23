#!/usr/bin/env python
import os
import gnupg
import sys
import getpass

#
# Script to decrypt the backed up files
# @author rahulsh1
#

# Decrypts the file using the given password
def decrypt(password, gpg_file):
    print("Decrypting " + gpg_file + "...")
    gpg_home = os.getenv("HOME") + "/.gpghome"
    gpg = gnupg.GPG(gnupghome=gpg_home)
    dest_file = os.path.splitext(gpg_file)[0]
    with open(gpg_file, 'rb') as f:
        status = gpg.decrypt_file(
            file=f,
            passphrase=password,
            output=dest_file)
    print('decryption ok: ', status.ok)
    #print('decryption status: ', status.status)
    #print('decryption stderr: ', status.stderr)
    print('~'*50)

def main():
    args = sys.argv[1:]
    if not args:
        print("usage: " + sys.argv[0] + " <file>");
        sys.exit(1)

    file = sys.argv[1]
    passphrase = getpass.getpass()
    decrypt(passphrase, file)

if __name__ == '__main__':
    main()

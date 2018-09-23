#!/usr/bin/env python

import os
from shutil import rmtree
import argparse
import logging
import sh
from sh import rsync
import gnupg

# Script to backup folders using rsync
# Works on *nix platforms only
# Original taken from https://github.com/AnonStar/home_backup
# Updates:
# 1. Removed global variables
# 2. Option to tgz the directories so they can be pushed to cloud
# 3. Option to encrypt the tgz with password
#

# Checks for existence of directory
def check_dir_exist(os_dir):
    if not os.path.exists(os_dir):
        logging.error("{} does not exist.".format(os_dir))
        exit(1)

# deletes the files with the given extensions
def delete_files(ending, indirectory):
    for r, d, f in os.walk(indirectory):
        for files in f:
            if files.endswith("." + ending):
                try:
                    os.remove(os.path.join(r, files))
                    logging.info("Deleting {}/{}".format(r, files))
                except OSError:
                    logging.warning("Could not delete {}/{}".format(r, files))
                    pass

# delete the trash files such as *.tmp, *.bak, *.dmp
def delete_trash(args):
    # Delete actual files first
    if args.trash:
        file_types = ["tmp", "bak", "dmp"]
        for file_type in file_types:
            delete_files(file_type, backupdir)
        # Empty trash can
        try:
            rmtree(os.path.expanduser("~/.local/share/Trash/files"))
        except OSError:
            logging.warning("Could not empty the trash or trash already empty.")
            pass

# Creates a tgz, deletes the directory if requested and encrypts with gpg too
def zip_it(args, sourcedir, destinationdir):
    tail = sourcedir.split('/')[-1:][0]
    dest_dir = destinationdir + tail
    dest_file = dest_dir + ".tgz"
    #print('tail = ' + tail + ' dest_file=' + dest_file)
    if args.zip or args.zipdel:
        sh.tar("-cvzf", dest_file, "-C", destinationdir, tail)
        logging.info("Created " + dest_file)

    if args.zipdel:
        sh.rm("-rf", dest_dir)

    if args.useremail:
        print("Encrypting " + dest_file + "...")
        gpg_file = dest_file + ".gpg"
        gpg_home = os.getenv("HOME") + "/.gpghome"
        gpg = gnupg.GPG(gnupghome=gpg_home)

        with open(dest_file, 'rb') as f:
            status = gpg.encrypt_file(
                file=f,
                recipients=[args.useremail],
                output=gpg_file)
        print('encryption ok: ', status.ok)
        #print('encryption status: ', status.status)
        #print('encryption stderr: ', status.stderr)
        print('~'*50)

# Main function that does the backup using rsync
def doBackup(logfile, exclusions, is_quiet, backupdir, destinationdir):
    # Do the actual backup
    logging.info("Starting rsync.")
    if logfile and exclusions and is_quiet:
        rsync("-auhv", exclusions, "--log-file={}".format(logfile), backupdir, destinationdir)
    elif logfile and exclusions:
        print(rsync("-auhv", exclusions, "--log-file={}".format(logfile), backupdir, destinationdir))
    elif is_quiet and exclusions:
        rsync("-av", exclusions, backupdir, destinationdir)
    elif logfile and is_quiet:
        rsync("-av", "--log-file={}".format(logfile), backupdir, destinationdir)
    else:
        rsync("-av", backupdir, destinationdir)

    logging.info("done.")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("BACKUPDIR", help="Specify the source directory to backup.")
    parser.add_argument("DESTINATIONDIR", help="Specify the directory where the backup is stored.")
    parser.add_argument("-e", "--exclude", help="Exlude the following directories from backup.", action="append")
    parser.add_argument("-l", "--logfile", help="Specify the logfile to monitor.")
    parser.add_argument("-q", "--quiet", help="Do not print to stdout.", action="store_true")
    parser.add_argument("-z", "--zip", help="Create tgz file for the directory", action="store_true")
    parser.add_argument("-zd", "--zipdel", help="Create tgz file for the directory and delete the directory", action="store_true")
    parser.add_argument("-u", "--encruseremail", help="Enable encryption with given user-email already configured")

    args = parser.parse_args()
    backupdir = args.BACKUPDIR
    destinationdir = args.DESTINATIONDIR
    logfile = args.logfile

    # Logging
    rootLogger = logging.getLogger()
    logFormatter = logging.Formatter("%(asctime)s - %(message)s")
    rootLogger.setLevel(logging.INFO)
    if logfile:
        fileHandler = logging.FileHandler(logfile)
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)
    if not args.quiet:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

    # handle exclusions
    exclusions = []
    if args.exclude:
        for argument in args.exclude:
            exclusions.append("--exclude={}".format(argument))

    # Check if source exist
    check_dir_exist(backupdir)
    # Delete all the trash if requested
    delete_trash(args)
    # Perform the backup now
    doBackup(logfile, exclusions, args.quiet, backupdir, destinationdir)

    # Perform zip and its related options
    zip_it(args, backupdir, destinationdir)

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    main()

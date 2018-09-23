# encrypted-backups
Backup directories in compressed encrypted form

Supports delta backup of individual directories, zipping up the directories and also optionally encrypting them.
This is supported for *nix platforms only.

## Prerequisites
- Python 3

Install the missing modules using `easy_install` or `pip`.

### For encryption, you need GPG
> OSX
brew install gpg
> Linux
apt install gpg

Then install
pip install python-gnupg

## Script

    ./backup_folders.py -h
    usage: backup_folders.py [-h] [-e EXCLUDE] [-l LOGFILE] [-q] [-z] [-zd] [-u USEREMAIL]
                          BACKUPDIR DESTINATIONDIR

    positional arguments:
     BACKUPDIR             Specify the source directory to backup.
     DESTINATIONDIR        Specify the directory where the backup is stored.

    optional arguments:
     -h, --help            show this help message and exit
     -e EXCLUDE, --exclude EXCLUDE
                           Exclude the following directories from backup.
     -l LOGFILE, --logfile LOGFILE
                           Specify the logfile.
     -q, --quiet           Do not print to stdout.
     -z, --zip             Create tgz file for the directory
     -zd, --zipdel         Create tgz file for the directory and delete the directory
     -u USEREMAIL, --encruseremail USEREMAIL
                           email-id for encryption purposes

## Examples

    # Backup 'my_dir_one' to '~/backup/full', logging to backup.log
    $ ./backup_folders.py -l backup.log ~/Documents/my_dir_one ~/backup/full/

    # Backup 'my_project' to '~/backup/full' skipping any directory with name 'target'
    $ ./backup_folders.py -e target -l backup.log ~/Documents/code/github/my_project ~/backup/full/

    # Backup 'my_dir_one' to '~/backup/full' in Quiet mode, logging to backup.log
    $ ./backup_folders.py -q -l backup.log ~/Documents/my_dir_one ~/backup/full/

    # Backup directory and also create a tgz file
    $ ./backup_folders.py -q -z -e target -l backup.log ~/Documents/code/github/my_project ~/backup/full/

    # Backup directory and also create a tgz file and delete the directory from backup folder
    $ ./backup_folders.py -q -z -zd -e target -l backup.log ~/Documents/code/github/my_project ~/backup/full/

### With encryption

    # Creating the backup
    $ ./backup_folders.py -q -e target -l backup.log -u user@domain ~/Documents/code/github/my_project ~/backup/encrypted/

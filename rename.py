import configparser
import os
from operations import Operations

# Load config file for global use
config = configparser.ConfigParser()
config.read('config.ini')


class Rename:
    def __init__(self, file):
        self.file = file
        self.keys = 'key.csv'
        self.correspondence_endings = 'correspondence_endings.txt'
        self.accounts = 'accounts.csv'
        self.entity = 'entity.csv'
        self.named_filename = 'named.txt'
        self.rename_filename = 'rename_files.txt'

    # creates a list to rename files
    def rename_file_list(self):
        sort_obj = Operations(self.file)
        if sort_obj.is_correct_file_format():
            with open(self.named_filename, 'a') as f:
                f.write(self.file)
                f.write('\n')
        else:
            with open(self.rename_filename, 'a') as f:
                f.write(self.file)
                f.write('\n')

    @staticmethod
    def file_rename(old, new):
        start = config.get("Locations", "scan_folder")
        new_file_path = os.path.join(start, new)
        old_file_path = os.path.join(start, old)
        os.rename(old_file_path, new_file_path)
        Operations.log_file(f'renamed {old} to {new}')

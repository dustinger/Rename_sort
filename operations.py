import configparser
import csv
import re


# load config file for global use
config = configparser.ConfigParser()
config.read('config.ini')


class Operations:
    def __init__(self, file):
        self.file = str(file)
        self.keys = 'key.csv'
        self.correspondence_endings = 'correspondence_endings.txt'
        self.accounts = 'accounts.csv'
        self.entity = 'entity.csv'

    def get_file_year(self):

        if self.file[:5].isnumeric() or self.file[:3].isalpha():
            return ''
        else:
            return self.file[:4]

    def get_file_month(self):
        if self.file[:5].isnumeric() or self.file[:3].isalpha():
            return ''
        else:
            return self.file[5:7]

    def get_full_entity_name(self):
        ent = []
        with open('entity.csv', 'r') as csv_ent:
            for line in csv_ent:
                line_elements = line.strip().split(',')
                second = line_elements[-3] + "," + line_elements[-2]
                first = line_elements[-5] + "," + line_elements[-4]
                second_name = str(second).strip().replace('"', '')
                first_name = str(first).strip().replace('"', '')
                ent.append(second_name)
                ent.append(first_name)
                full_name = line_elements[0] + "," + line_elements[1]
                full = str(full_name).strip().replace('"', '')
                ent.append(full)
        name_list = ent
        reg = "|".join(re.escape(name) for name in name_list)  # Create a regex pattern with all names from the list
        match = re.search(reg, self.file)
        if match:
            return match.group(0)
        return ''

    def get_family_name(self):
        ent = []
        with open('entity.csv', 'r') as csv_ent:
            for line in csv_ent:
                line_elements = line.strip().split(',')
                full_name = line_elements[0] + "," + line_elements[1]
                full = str(full_name).strip().replace('"', '')
                ent.append(full)
        name_list = ent
        reg = "|".join(re.escape(name) for name in name_list)  # Create a regex pattern with all names from the list
        match = re.search(reg, self.file)
        if match:
            return match.group(0)
        return ''

    def get_account_number_list(self):
        # gets account number list
        acct = []
        with open('accounts.csv', 'r') as csv_ent:
            for line in csv_ent:
                line_elements = line.strip().split(',')
                account_number = [element for element in line_elements if element.isalnum() and (
                        element.isdigit() or (len(element) >= 3 and element[:3].isalpha()))]
                if account_number:
                    acct.append(account_number[0])
                else:
                    acct.append("N/A")
        acct_list = acct
        reg = "|".join(re.escape(name) for name in acct_list)  # Create a regex pattern with all names from the list
        match = re.search(reg, self.file)
        if match:
            return match.group(0)
        return ''

    def get_date(self):
        date_regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
        match = re.search(date_regex, self.file)
        if match:
            return match.group(0)
        else:
            return ''

    def get_key(self):
        with open(self.keys, 'r', newline='') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                reg = row[0]  # Assuming you want to search in the first column
                match = re.search(reg, self.file)
                if match:
                    return match.group(0)
        return ''

    def get_key_location(self):
        with open(self.keys,'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) >= 2:  # Ensure the row has at least two columns (first and second)
                    account_number = row[0]
                    if re.search(account_number, self.file):
                        return row[1]
        return False

    def get_keyword_year(self):
        with open(self.keys,'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) >= 5:  # Ensure the row has at least two columns (first and second)
                    account_number = row[0]
                    if re.search(account_number, self.file):
                        return row[4]

    def is_key(self):
        target_key = self.get_key()  # Get the key from the keys.csv file
        if target_key != '':
            with open(self.keys, 'r', newline='') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if row[0] == target_key:  # Check if the key exists in the keys.csv file
                        return True
        return False

    def get_correspondence_endings(self):
        with open(self.correspondence_endings, 'r') as f:
            regex_patterns = f.read().splitlines()
        for pattern in regex_patterns:
            match = re.search(pattern, self.file)
            if match:
                return match.group(0)

        return ''

    def is_incoming(self):
        content = self.get_correspondence_endings()
        return "in" in content

    def get_account_folder(self):
        # gets Account Folder Name
        with open(self.accounts, 'r', newline='') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) >= 2:  # Ensure the row has at least two columns (first and second)
                    account_number = row[1]  # Assuming the account number is in the second column (index 1)
                    if re.search(account_number, self.file):
                        return row[0]  # Return the corresponding result from the first column (index 0)
        return False

    def get_account_family(self):
        # gets family name from account number
        with open(self.accounts, 'r', newline='') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) >= 3:  # Ensure the row has at least three columns (first, second, and third)
                    family_name = row[1]  # Assuming the family name is in the third column (index 2)
                    if re.search(family_name, self.file):
                        return row[2]  # Return the corresponding result from the first column (index 0)
        return False

    def is_correct_file_format(self):
        date_part = self.get_date()
        entity_part = self.get_full_entity_name()
        account_part = self.get_account_number_list()
        keyword_part = self.get_key()
        correct = f'{date_part} {entity_part} {account_part} {keyword_part}'
        # correct file format date entity account keyword correspondence
        # Check if all parts are non-empty and present in the file name
        if date_part and entity_part and account_part and keyword_part:
            if date_part in self.file and entity_part in self.file \
                    and account_part in self.file and keyword_part in self.file:
                if correct == self.file:
                    return True
        return False


def log_file(message):
    with open('log.txt','a') as log:
        log.write(message)


def first_entity_name():
    ent = []
    col1_index = 1
    col2_index = 2
    with open('entity.csv', 'r') as csv_ent:
        csv_reader = csv.reader(csv_ent)
        for row in csv_reader:
            # Assuming col1_index and col2_index are 0-based indices
            if len(row) > max(col1_index, col2_index):
                if not row[col1_index] == '':
                    ent.append(row[col1_index].rsplit(',')[1])
                if not row[col2_index] == '':
                    ent.append(row[col2_index].rsplit(',')[1])
    ent.sort()
    return ent


def full_name_list():
    ent = []
    col1_index = 1
    col2_index = 2
    with open('entity.csv', 'r') as csv_ent:
        csv_reader = csv.reader(csv_ent)
        for row in csv_reader:
            # Assuming col1_index and col2_index are 0-based indices
            if len(row) > max(col1_index, col2_index):
                if not row[col1_index] == '':
                    ent.append(row[col1_index])
                if not row[col2_index] == '':
                    ent.append(row[col2_index])
            ent.append(row[0])
    ent = list(set(ent))
    ent.sort()
    return ent

def family_name_list():
    ent = []
    col1_index = 0

    with open('entity.csv', 'r') as csv_ent:
        csv_reader = csv.reader(csv_ent)
        for row in csv_reader:
            # Assuming col1_index and col2_index are 0-based indices
            if len(row) > col1_index:
                if not row[col1_index] == '':
                    ent.append(row[col1_index])
    ent.sort()
    return ent


def keywords_location_list():
    key = []
    col1_index = 0

    with open('new_folders.txt', 'r') as csv_ent:
        csv_reader = csv.reader(csv_ent)
        for row in csv_reader:
            # Assuming col1_index and col2_index are 0-based indices
            r = str(row)
            key.append(r)
    return key


print(keywords_location_list())

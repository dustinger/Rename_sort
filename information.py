import configparser
import os
import re


config = configparser.ConfigParser()
con = config.read('config.ini')

# Person Class creates family name, folder and parses family name
class Person:
    def __init__(self, first_name, last_name, spouse_first_name, spouse_last_name, status):
        self.first_name = first_name
        self.last_name = last_name
        self.spouse_first_name = spouse_first_name
        self.spouse_last_name = spouse_last_name
        self.status = status
        self.entity_locations = config.get("Locations", "entity_folder")
        self.closed_entity_locations = config.get("Locations", "closed_entity")
        self. entity_list = "entity.csv"

    # take the names of clients and combines them into a family name
    def create_family_name(self):
        name_parts = []
        if self.first_name and self.last_name:
            name_parts.append(f"{self.last_name}, {self.first_name}")
        elif self.last_name:
            name_parts.append(self.last_name)
        if self.spouse_first_name:
            if self.spouse_last_name and self.spouse_last_name != self.last_name:
                name_parts.append(f"and {self.spouse_last_name}, {self.spouse_first_name}")
            else:
                name_parts.append(f"and {self.spouse_first_name}")
        entity = ' '.join(name_parts)
        return entity

# creates an entity folder depending on if entity is a current entity or closed
    def create_entity_folder(self):
        start = self.entity_locations
        closed_start = self.closed_entity_locations
        name = self.create_family_name()
        open_path = os.path.join(start, name)
        closed_path = os.path.join(closed_start, name)
        if not self.status:
            if not os.path.exists(open_path):
                os.mkdir(open_path)
        else:
            if not os.path.exists(closed_path):
                os.mkdir(closed_path)

# gets individuals names from family name
    @staticmethod
    def separate_family_name(family_name):
        first_name = None
        last_name = None
        spouse_first_name = None
        spouse_last_name = None

        # Regular expressions to match the various patterns in the family name
        patterns = [
            r'^(?P<last_name>[^,]+), (?P<first_name>[^ ]+)$',
            r'^(?P<last_name>[^,]+)$',
            r'^(?P<last_name>[^,]+), (?P<first_name>[^ ]+) and (?P<spouse_last_name>[^,]+), (?P<spouse_first_name>[^ ]+)$',
            r'^(?P<last_name>[^,]+), (?P<first_name>[^ ]+) and (?P<spouse_first_name>[^ ]+)$',
            r'^(?P<last_name>[^,]+) and (?P<spouse_last_name>[^,]+), (?P<spouse_first_name>[^ ]+)$',
            r'^(?P<last_name>[^,]+) and (?P<spouse_first_name>[^ ]+)$'
        ]

        for pattern in patterns:
            match = re.match(pattern, family_name)
            if match:
                groups = match.groupdict()
                first_name = groups.get('first_name')
                last_name = groups.get('last_name')
                spouse_first_name = groups.get('spouse_first_name')
                spouse_last_name = groups.get('spouse_last_name')
                break

        return f'{last_name}, {first_name}', f'{spouse_first_name}.{spouse_last_name}'

# Account Class creates account name, folder and parses account name
class Account:
    def __init__(self,company, acct_number, kind, first_name, family_name, status):
        self.company = company
        self.acct_number = acct_number
        self.kind = kind
        self.first_name = first_name
        self.family_name = family_name
        self.status = status
        self.entity_locations = config.get("Locations", "entity_folder")
        self.closed_entity_locations = config.get("Locations", "closed_entity")

    def account_name(self):
        return f'{self.company}, {self.acct_number} {self.first_name}'

    def create_account_folder(self):
        start = self.entity_locations
        closed_start = self.closed_entity_locations
        name = self.account_name()
        open_path = os.path.join(start, name)
        closed_path = os.path.join(closed_start, name)
        if not self.status:
            if not os.path.exists(open_path):
                os.mkdir(open_path)
        else:
            if not os.path.exists(closed_path):
                os.mkdir(closed_path)

    @staticmethod
    def seperate_name(account_name):
        company = None
        account = None
        name = None
        pattern = r'(?P<company>[A-Za-z]+),\s(?P<account>[0-9A-Za-z]+)\s(?P<name>[0-9A-Za-z]+)'
        match = re.match(pattern, account_name)
        if match:
            groups = match.groupdict()
            company = groups.get('company')
            account = groups.get('account')
            name = groups.get('name')
        return company, account, name


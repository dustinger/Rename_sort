import operations
import os
import configparser
from shutil import move, copy


config = configparser.ConfigParser()
config.read('config.ini')
main_incoming = config.get('Locations', 'Main_Incoming')
main_outgoing = config.get('Locations', 'Main_Outgoing')
completed_documents = config.get('Locations', 'Completed_Documents')
entity_folder = config.get('Locations', 'Entity_Folder')
working_documents = config.get('Locations', 'Working_Documents')
closed_entity_folder = config.get('Locations', 'Closed_Entity')
scan_folder = config.get('Locations', 'scan_folder')
entity_incoming = config.get('Locations', 'entity_incoming')
entity_outgoing = config.get('Locations', 'entity_outgoing')


def main_mail_location(file):
    ops = operations.Operations(file)
    if ops.is_incoming():
        location = main_incoming
    else:
        location = main_outgoing
    final = os.path.join(location, file)
    if os.path(final).exists():
        return final
    return ''


def entity_location(file):
    ops = operations.Operations(file)
    entity = ops.get_family_name()
    final = os.path.join(entity_folder, entity)
    if os.path(final).exists():
        return final
    return ''


def account_location(file):
    ops = operations.Operations(file)
    acct_folder_name = ops.get_account_folder()
    family = ops.get_account_family()
    if not family:  # Handle the case when family is False (e.g., family name not available)
        return ''
    acct_standard_location = 'RIA Folder/Accounts'
    final = os.path.join(family, acct_standard_location, acct_folder_name)
    if os.path(final).exists():
        return final
    return ''


def keyword_location(file):
    # how the key.csv is set up key, location, account_folder, working_documents, year_folder
    ops = operations.Operations(file)
    key_location = ops.get_key_location()
    family = ops.get_family_name()
    final = os.path.join(family, key_location)
    if os.path(final).exists():
        return final
    return ''


def entity_correspondence_location(file):
    ops = operations.Operations(file)
    if ops.is_incoming():
        location = entity_incoming
    else:
        location = entity_outgoing
    entity = entity_folder(file)
    final = os.path.join(entity, location)
    if os.path(final).exists():
        return final
    return ''


def sort(file):
    ops = operations.Operations(file)
    year_file = ops.get_file_year()
    month_file = ops.get_file_month()
    old = os.path.join(scan_folder, file)
    main_correspondence = os.path.join(main_mail_location(file), year_file, month_file)
    account = account_location(file)
    keyword = keyword_location(file)
    entity_correspondence = os.path.join(entity_correspondence_location(file), year_file)
    completed = os.path.join(os.path.join(completed_documents, year_file), month_file)  # Corrected variable name
    copy(old, main_correspondence)
    operations.log_file(f'Copied {file} to {main_correspondence}')
    copy(old, account)
    operations.log_file(f'Copied {file} to {account}')
    copy(old, keyword)
    operations.log_file(f'Copied {file} to {keyword}')
    copy(old, entity_correspondence)
    operations.log_file(f'Copied {file} to {entity_correspondence}')
    move(old, completed)
    operations.log_file(f'Moved {file} to {completed}')

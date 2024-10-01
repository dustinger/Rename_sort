import os


# entity.csv(Family name, closed)
def create_missing_files():
    file_paths = ['new_account_folders.txt', 'correspondence_endings.txt', 'log.txt', 'named.txt', 'entity.csv',
                  'new_folders.txt', 'key.csv', 'accounts.csv', 'rename_files.txt']
    for file_path in file_paths:
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write("")
                print(f'created:{file_path}')

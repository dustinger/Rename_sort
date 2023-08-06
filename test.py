from faker import Faker
from information import Person, Account, Keyword
import operations
import sort


fake = Faker()
closed = fake.boolean(chance_of_getting_true=45)


def fake_entities():
    last_name = fake.last_name()
    spouse_last_name = np.random.choice([fake.last_name(), ''])  # Fix for NumPy output
    first_name = fake.first_name()
    spouse_first_name = np.random.choice([fake.first_name(), ''])  # Fix for NumPy output
    company = fake.company()
    acct_number = fake.swift11()
    entity = Person(first_name, last_name, spouse_first_name, spouse_last_name, False)
    entity.create_entity_folder()
    acct = Account(company, acct_number, "Roth", entity.get_first_name(), entity.family_name())
    acct.create_account_folder()


import tkinter as tk
from tkinter import ttk


def test():
    folder = []
    table = [True, False]

    # Read values from 'new_folders.txt' and store them in the 'folder' list
    with open('new_folders.txt', 'r') as f:
        for line in f:
            folder.append(line.strip())

    def on_selection_change(event):
        # This function will be called when the selection in the dropdown changes
        selected_value = selected_option.get()
        print("Selected Value:", selected_value)

    def on_keyword_entry(event):
        # This function will be called when a keyword is entered in the Entry field
        keyword_value = key.get()
        print("Keyword:", keyword_value)


    root = tk.Tk()
    root.title("Dropdown Menu Example")

    selected_option = tk.StringVar()
    selected_account_folder = tk.StringVar()
    selected_working_folder = tk.StringVar()
    selected_year_folder = tk.StringVar()

    location_label = ttk.Label(root, text="Location:")
    location_label.grid(row=0, column=0, padx=10, pady=5)

    key_locations = ttk.Combobox(root, textvariable=selected_option, values=folder)
    key_locations.grid(row=0, column=1, padx=10, pady=5)
    key_locations.bind("<<ComboboxSelected>>", on_selection_change)

    key_label = ttk.Label(root, text="Keyword:")
    key_label.grid(row=1, column=0, padx=10, pady=5)

    key = ttk.Entry(root)
    key.grid(row=1, column=1, padx=10, pady=5)
    key.bind("<Return>", on_keyword_entry)  # Bind the Enter key press event to the keyword entry field

    account_label = ttk.Label(root, text="Account Folder")
    account_label.grid(row=2, column=0, padx=10, pady=5)
    account_folder = ttk.Combobox(root, textvariable=selected_account_folder, values=table)
    account_folder.grid(row=2, column=1, padx=10, pady=5)

    working_label = ttk.Label(root, text="Working Documents Folder")
    working_label.grid(row=3, column=0, padx=10, pady=5)
    working_folder = ttk.Combobox(root, textvariable=selected_working_folder, values=table)
    working_folder.grid(row=3, column=1, padx=10, pady=5)

    year_label = ttk.Label(root, text="Year Folder")
    year_label.grid(row=4, column=0, padx=10, pady=5)
    year_folder = ttk.Combobox(root, textvariable=selected_year_folder, values=table)
    year_folder.grid(row=4, column=1, padx=10, pady=5)

    def create():
        # Get the values from the dropdowns and the text entry field
        key_location = selected_option.get()
        account_folder_value = selected_account_folder.get()
        working_folder_value = selected_working_folder.get()
        year_folder_value = selected_year_folder.get()
        key_value = key.get()

        # Create a new keyword object and call the method to create the key info
        keys = Keyword(key_value, key_location, account_folder_value, working_folder_value, year_folder_value)
        keys.create_key_info()

    create_new_key = ttk.Button(root, text="Add a Keyword", command=create)
    create_new_key.grid(row=5, column=0, padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    test()

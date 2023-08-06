import configparser
import tkinter as tk
from tkinter import filedialog


def repeat_program():
    config = configparser.ConfigParser()
    config.read('config.ini')
    setup = config.getboolean('program', 'setup')
    try:
        if setup:
            # Code to run if the setup has already been completed
            print("Setup has already been completed.")
            main_incoming = config.get('Locations', 'Main_Incoming')
            main_outgoing = config.get('Locations', 'Main_Outgoing')
            completed_documents = config.get('Locations', 'Completed_Documents')
            entity_folder = config.get('Locations', 'Entity_Folder')
            working_documents = config.get('Locations', 'Working_Documents')
            closed_entity_folder = config.get('Locations', 'Closed_Entity')
            print("Main Incoming:", main_incoming)
            print("Main Outgoing:", main_outgoing)
            print("Completed Documents:", completed_documents)
            print("Entity Folder:", entity_folder)
            print("Working Documents:", working_documents)
            print("Closed Entity:", closed_entity_folder)
        else:
            # Code to run if the setup has not been completed
            config['program']['setup'] = 'True'  # Update the setup value
            config['Locations'] = {
                'Main_Incoming': filedialog.askdirectory(title="Select Main Incoming folder"),
                'Main_Outgoing': filedialog.askdirectory(title="Select Main Outgoing folder"),
                'Completed_Documents': filedialog.askdirectory(title="Select Completed Documents folder"),
                'Entity_Folder': filedialog.askdirectory(title="Select Entity Folder"),
                'Working_Documents': filedialog.askdirectory(title="Select Working Documents folder"),
                'Scan_folder': filedialog.askdirectory(title="Select Scan Folder"),
                'Closed_Entity': filedialog.askdirectory(title="Select Closed Entity Folder"),
                'entity_incoming': 'Client Communication / Incoming',
                'entity_outgoing': 'Client Communication / Outgoing'
            }

            with open('config.ini', 'w') as configfile:
                config.write(configfile)

    except configparser.Error as e:
        print("Error reading configuration:", e)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    repeat_program()

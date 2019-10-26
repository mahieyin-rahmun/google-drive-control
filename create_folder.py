import json
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Auth import Auth, SCOPES

def create_student_folders(service, student_ids, parent_folder):
    if parent_folder is None:
        raise Exception("Parent folder must be specified...")
    # against each of the student id
    for student_id in student_ids:
        student_folder_metadata = {
            'name': student_id,
            'parents': [parent_folder.get('id')],
            'mimeType': 'application/vnd.google-apps.folder'
        }        
        # create a folder with the id as the name
        student_folder = service.files().create(body=student_folder_metadata, fields='id').execute()
        
        print(f"Student folder '{student_id}' created with id {student_folder.get('id')} under {parent_folder}")
    
    


def create_nested_folder_structure(service, parent_folder, folder_prefix, student_ids, folder_suffix_lower_limit=1):
    number_of_folders = int(input("Enter number of folders to create: "))
    
    folder_nums = [i for i in range(folder_suffix_lower_limit, number_of_folders + 1)]
    
    for folder_num in folder_nums:
        folder_name = f'{folder_prefix} #{folder_num}'
      
        folder_metadata = {
            'name': folder_name,
            'parents': [parent_folder.get('id')],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        
        print(f"{folder_prefix} folder {folder_name} created under parent folder with id {folder.get('id')}")
        
        create_student_folders(service, student_ids, folder)


def main():
    """
        This script deals with creating a nested folder structure
        
        Parent Folder
        |_ <Prefix> #1
        |_ Student ID #1
        |_ Student ID #2
        |_ Student ID #3
        |_ ...
        |_ <Prefix> #2
        |_ Student ID #1
        |_ Student ID #2
        |_ Student ID #3
        |_ ...
        |_ ...
        
        if prefix is not specified, it will create a folder structure like this
        
        Parent Folder
        |_ Student ID #1
        |_ Student ID #2
        |_ Student ID #3
        |_ ...
    """
    
    # get authorization if not authorized
    authorizer = Auth(SCOPES, os.path.join(os.path.abspath('.'), './credentials'), os.path.join(os.path.abspath('.'), './pickled_creds'))
    service = authorizer.authorize()
    
    parent_folder_name = input("Enter parent folder name: ")
    
    # creates one folder with the given name
    parent_metadata = {
        'name': parent_folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }  
    parent_folder = service.files().create(body=parent_metadata, fields='id').execute()
    
    print(f"Parent folder {parent_folder_name} created with id={parent_folder.get('id')}")
    
    # read json file, where student ids are stored in an array form
    with open(os.path.join(os.path.abspath('.'), './student_ids/students.json'), 'r') as students_id_file:
        # get the student ids
        student_ids = json.load(students_id_file)
        
        folder_prefix = input("Enter folder prefix: ")
        
        if folder_prefix != '':
            create_nested_folder_structure(service, parent_folder, folder_prefix, student_ids)
        else:
            create_student_folders(service, student_ids, parent_folder)



if __name__ == "__main__":
  main()
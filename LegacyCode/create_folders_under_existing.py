import json
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Auth import Auth, SCOPES
from search_folder import get_folder_id_by_name
from create_folder import create_student_folders, create_nested_folder_structure

def main():
    parent_folder = get_folder_id_by_name(get_id_only=False)
    
    authorizer = Auth(SCOPES, os.path.join(os.path.abspath('.'), './credentials'), os.path.join(os.path.abspath('.'), './pickled_creds'))
    service = authorizer.authorize()
    
    with open(os.path.join(os.path.abspath('.'), './student_ids/students.json'), 'r') as students_id_file:
        # get the student ids
        student_ids = json.load(students_id_file)
        
        folder_prefix = input("Enter folder prefix: ")
        
        if folder_prefix != '':
            lower_limit = input("Are there existing folders? If so, enter the value of suffix to start from: ")
            if lower_limit != '':                
                create_nested_folder_structure(service, parent_folder, folder_prefix, student_ids, folder_suffix_lower_limit=int(lower_limit))
            else:
                create_nested_folder_structure(service, parent_folder, folder_prefix, student_ids)
        else:
            create_student_folders(service, student_ids, parent_folder)
         
    
if __name__ == "__main__":
    main()
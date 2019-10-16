import json
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Auth import Auth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file', 
          'https://www.googleapis.com/auth/drive.metadata']

def main():
  """
    This script deals with creating a nested folder structure
    
    Parent Folder
    |_ Assignment #1
      |_ Student ID #1
      |_ Student ID #2
      |_ Student ID #3
      |_ ...
    |_ Assignment #2
      |_ Student ID #1
      |_ Student ID #2
      |_ Student ID #3
      |_ ...
    |_ ...
  """
  
  # get authorization if not authorized
  authorizer = Auth(SCOPES, os.path.join(os.path.abspath('.'), './credentials'), os.path.join(os.path.abspath('.'), './pickled_creds'))
  service = authorizer.authorize()
  
  # creates one folder with the given name
  parent_metadata = {
    'name': 'CSE215.3L SAS3 Fall 2019 Assignment Submissions',
    'mimeType': 'application/vnd.google-apps.folder'
  }  
  parent_folder = service.files().create(body=parent_metadata, fields='id').execute()
  
  print(f"Parent folder CSE215.3L Assignments created with id={parent_folder.get('id')}")
  
  # read json file, where student ids are stored in an array form
  with open(os.path.join(os.path.abspath('.'), './student_ids/students.json'), 'r') as students_id_file:
    # get the student ids
    student_ids = json.load(students_id_file)
    
    # for now we want to create 11 assignment folders inside every students folder
    assignment_nums = [i for i in range(1, 12)]
    
    for assignment_num in assignment_nums:
      assignment_folder_name = f'Assignment #{assignment_num}'
      
      assignment_folder_metadata = {
        'name': assignment_folder_name,
        'parents': [parent_folder.get('id')],
        'mimeType': 'application/vnd.google-apps.folder'
      }
      assignment_folder = service.files().create(body=assignment_folder_metadata, fields='id').execute()
      
      print(f"Assignment folder {assignment_folder_name} created under parent folder with id {assignment_folder.get('id')}")    
    
      # against each of the student id
      for student_id in student_ids:
        student_folder_metadata = {
          'name': student_id,
          'parents': [assignment_folder.get('id')],
          'mimeType': 'application/vnd.google-apps.folder'
        }        
        # create a folder with the id as the name
        student_folder = service.files().create(body=student_folder_metadata, fields='id').execute()
        
        print(f"Student folder '{student_id}' created with id {student_folder.get('id')} under {assignment_folder_name}")
  
if __name__ == "__main__":
  main()
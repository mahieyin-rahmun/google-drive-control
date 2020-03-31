import os
import json
import sys

from abc import ABC, abstractmethod

from Auth import Auth


class Flow(ABC):
    __required_folders = [
        os.path.join(os.path.abspath('.'), 'credentials'),
        os.path.join(os.path.abspath('.'), 'pickled_creds')
    ]

    # If modifying these scopes, delete the file token.pickle.
    __SCOPES = [
			'https://www.googleapis.com/auth/drive.file',
		  	'https://www.googleapis.com/auth/drive.metadata',
		  	'https://www.googleapis.com/auth/drive'
		  ]


    def __init__(self):
        self.__create_necessary_folders__()
        self.__authorize__()
        self.__get_path_to_students_file__()
        self.__extract_student_ids__()


    def __get_path_to_students_file__(self):
        students_file_path = input("Please enter the full path to students.json file: ")
        students_file_path = students_file_path.replace("\\", "\\\\")
        print("File path given: " + students_file_path)

        try:
            if not os.path.isfile(students_file_path) and not students_file_path.endswith('.json'):
                raise Exception("Invalid file/path.")

            self.students_file_path = students_file_path
        except Exception as e:
            print(str(e))
            sys.exit(-1)            

    
    def __extract_student_ids__(self):
        with open(self.students_file_path, "r") as students_json_file:
            try:
                student_ids = json.load(students_json_file)
            except json.JSONDecodeError:
                raise Exception("The json file is not valid.")
            else:
                self.student_ids = student_ids


    def __create_necessary_folders__(self):
        for folder_path in Flow.__required_folders:
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)


    def __authorize__(self):
        try:
            authorizer = Auth(Flow.__SCOPES, *Flow.__required_folders)
            service = authorizer.authorize()
            self.service = service
        except Exception as e:
            print(str(e))
            sys.exit(-1)

    def get_service(self):
        if self.service:
            return self.service

    
    def get_students_file_path(self):
        if self.students_file_path:
            return self.students_file_path


    def get_student_ids(self):
        if self.student_ids:
            return self.student_ids


    @abstractmethod
    def execute(self):
        pass


    def run(self):
        self.execute()

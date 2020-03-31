from tqdm import tqdm
from Flow import Flow

class CreateFolders(Flow):

	def __init__(self):
		super().__init__()
		

	def __create_parent_folder__(self):
		service = self.get_service()

		parent_folder_name = input("Enter parent folder name: ")

		if (parent_folder_name == ""):
			raise Exception("Parent folder name cannot be empty.")
		
		# creates one folder with the given name
		parent_metadata = {
			'name': parent_folder_name,
			'mimeType': 'application/vnd.google-apps.folder'
		}

		parent_folder = service.files().create(body=parent_metadata, fields='id').execute()
		print(f"Parent folder {parent_folder_name} created.")

		return parent_folder

	
	def __create_students_folders__(self, parent_folder=None):
		if not parent_folder:
			raise Exception("Parent folder must be specified...")
		
		service = self.get_service()

		student_ids = self.get_student_ids()

		for student_id in tqdm(student_ids):
			student_folder_metadata = {
				'name': student_id,
				'parents': [parent_folder.get('id')],
				'mimeType': 'application/vnd.google-apps.folder'
			}        
			# create a folder with the id as the name
			student_folder = service.files().create(body=student_folder_metadata, fields='id').execute()


	def __create_nested_folder_structure__(self, parent_folder, sub_dirs_name_prefix, suffix, num_folders):
		service = self.get_service()

		for folder_suffix in range(suffix, num_folders + 1):
			folder_name = f'{sub_dirs_name_prefix} #{folder_suffix}'

			folder_metadata = {
				'name': folder_name,
				'parents': [parent_folder.get('id')],
				'mimeType': 'application/vnd.google-apps.folder'
			}

			folder = service.files().create(body=folder_metadata, fields='id').execute()

			print(f"{folder_name} created.")

			self.__create_students_folders__(parent_folder=folder)




	
	def __get_subdir_prefix__(self):
		sub_dirs_name = input("Please enter the prefix of the folder(s) to be created inside the parent folder: ")

		if (sub_dirs_name != ""):			
			return sub_dirs_name
		
		return None

	
	def __get_suffix__(self):
		suffix = input("Are there existing folders? If so, please enter the number to start from: ")

		if (suffix != ""):
			try:
				int(suffix)
			except ValueError:
				raise Exception("Suffix must be an integer.")
			else:
				return int(suffix)

		# start the numbering from 1
		return 1


	def __get_num_folders_to_create__(self):
		num_folders = input("Enter the number of folders to create: ")

		if (num_folders == ""):
			raise Exception("Number of folders is required.")

		try:
			int(num_folders)
		except ValueError:
			raise Exception("Number of folders must be numeric.")
		else:
			if int(num_folders) <= 0:
				raise Exception("Number of folders cannot be negative or zero.")

			return int(num_folders)
		

	def execute(self):
		# ask about the parent folder name
		parent_folder = self.__create_parent_folder__()
		sub_dirs_name_prefix = self.__get_subdir_prefix__()

		if not sub_dirs_name_prefix:
			# the user only wants to create student folders inside the parent folder
			self.__create_students_folders__(parent_folder=parent_folder)
		else:
			# user wants to create a nested folder structure
			suffix = self.__get_suffix__()
			num_folders = self.__get_num_folders_to_create__() 
			self.__create_nested_folder_structure__(parent_folder, sub_dirs_name_prefix, suffix, num_folders)
				

			



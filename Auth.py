import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Auth:
  def __init__(self, SCOPES, cred_save_path, token_save_path, port=0):
    self.SCOPES = SCOPES
    self.port = port
    self.cred_save_path = cred_save_path
    self.token_save_path = token_save_path
    
  def authorize(self):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(self.token_save_path, 'token.pickle')):
        with open(os.path.join(self.token_save_path, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.join(self.cred_save_path, 'credentials.json'), self.SCOPES)
            creds = flow.run_local_server(port=self.port)
        # Save the credentials for the next run
        with open(os.path.join(self.token_save_path, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)    
    return service
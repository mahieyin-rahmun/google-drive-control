import json
import os
from pprint import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Auth import Auth, SCOPES

def grant_permission(file_id, email):
    authorizer = Auth(SCOPES, os.path.join(os.path.abspath('.'), './credentials'), os.path.join(os.path.abspath('.'), './pickled_creds'))
    service = authorizer.authorize()
 
    request_body = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': email
    }
    
    results = service.permissions().create(fileId=file_id, body=request_body, fields='emailAddress,id').execute()
    print(results)
    



if __name__ == "__main__":
    folder_id = '1asQvQgIl5NBHL9v4WW3KUTgmw8jxNi5C'
    grant_permission(folder_id, "mahieyin.rahmun@gmail.com")
    
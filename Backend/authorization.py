import datastoreMethods as dataMethods
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.cloud import datastore

SCOPES = ['https://www.googleapis.com/auth/gmail.addons.current.action.compose',
          'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/datastore', 'https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/drive.metadata']


def dev_authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization.py flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_v1.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def authenticate():
    creds = None
    client = datastore.Client("driveaddon-2122")
    token = dataMethods.get_most_recent_token(client)
    if token is not None:
        creds = Credentials.from_authorized_user_info(token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            client = datastore.Client("driveaddon-2122", credentials=creds)
            dataMethods.store_token(client, creds)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_v1.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        client = datastore.Client("driveaddon-2122", credentials=creds)
        dataMethods.store_token(client, creds)

    return creds

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.cloud import datastore
import Backend.datastoreMethods as dataMethods

SCOPES = ['https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/datastore', 'https://www.googleapis.com/auth/drive']


# Authenticate the addon.
# Acquires tokens from the datastore, if it exists.
# If there is no token, then create a new token
# and save the new token to the datastore.
# If there is a token but it is expired,
# then it refreshes the token and save it in the datastore.
#
# Returns:
#   The acquired/created credentials.
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
                'Backend/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            client = datastore.Client("driveaddon-2122", credentials=creds)
            dataMethods.store_token(client, creds)

    return creds

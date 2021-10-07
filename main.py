import base64
import json
import os
from datetime import datetime
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.cloud import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build
from google.cloud import datastore


#
#  Google Cloud Function that loads the homepage for a
#  Google Workspace Add-on.
#
#  @param {Object} req Request sent from Google
#
def load_homepage(req):
    return create_action()


# Creates a card with two widgets.
def create_action():
    card = {
        "action": {
            "navigations": [
                {
                    "pushCard": {
                        "header": {
                            "title": "Cats!"
                        },
                        "sections": [
                            {
                                "widgets": [
                                    {
                                        "textParagraph": {
                                            "text": "Your random cat:"
                                        }
                                    },
                                    {
                                        "image": {
                                            "imageUrl": "https://aiptcomics.com/wp-content/uploads/2019/09/JUL190885.jpg"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }
    return json.dumps(card)


def authenticate():
    scopes = ['https://www.googleapis.com/auth/gmail.addons.current.action.compose',
              'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.compose',
              'https://www.googleapis.com/auth/datastore']
    creds = None
    client = datastore.Client("driveaddon-2122")
    token = get_most_recent_token(client)
    creds = Credentials.from_authorized_user_info(token, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            client = datastore.Client("driveaddon-2122", credentials=creds)
            store_token(client, creds)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        client = datastore.Client("driveaddon-2122", credentials=creds)
        store_token(client, creds)

    return creds


def create_service(addon_name, version, creds):
    service = build(addon_name, version, credentials=creds)
    return service


# Create a message for an email.
#
# Args:
#   sender: Email address of the sender.
#   to: Email address of the receiver.
#   subject: The subject of the email message.
#   message_text: The text of the email message.
#
# Returns:
#   An object containing a base64url encoded email object.
def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['from'] = sender
    message['to'] = to
    message['subject'] = subject
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    return {'raw': b64_string}


#   Send an email message.
#
# Args:
#   service: Authorized Gmail API service instance.
#   user_id: User's email address. The special value "me"
#   can be used to indicate the authenticated user.
#   message: Message to be sent.
#
# Returns:
#   Sent Message.
def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def create_widgets():
    widgets = {
        "widgets": [
            {
                "textParagraph": {
                    "text": ""
                }
            },
            {
                "image": {
                    "imageUrl": "https://cataas.com/cat"
                }
            }
        ]
    }
    return widgets


def create_sections():
    sections = create_widgets()
    return sections


def create_push_card():
    push_card = {
        "header": {
            "title": "rgarsgaragw"
        },
        "sections": create_sections()
    }
    return push_card


def create_card(title, icon_url):
    card = {
        "action": {
            "navigations": [
                {
                    "pushCard": {
                        "header": {
                            "title": title
                        },
                        "sections": [
                            {
                                "widgets": [
                                    {
                                        "textParagraph": {
                                            "text": "The icon is:"
                                        }
                                    },
                                    {
                                        "image": {
                                            "imageUrl": icon_url
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }
    return json.dumps(card)


def store_token(client: datastore.Client, creds):
    key = client.key("Token")
    token = datastore.Entity(key)
    json_creds = creds.to_json()
    loaded_creds = json.loads(json_creds)
    token.update({
        "created": datetime.now(),
        "token": loaded_creds["token"],
        "refresh_token": loaded_creds["refresh_token"],
        "token_uri": loaded_creds["token_uri"],
        "client_id": loaded_creds["client_id"],
        "client_secret": loaded_creds["client_secret"],
        "scopes": loaded_creds["scopes"],
        "expiry": loaded_creds["expiry"]
    })
    client.put(token)


def get_most_recent_token(client: datastore.Client):
    query = client.query(kind="Token")
    query.order = ["created"]
    results = list(query.fetch())
    return results[len(results)-1]


# To use logging:
#   logger = logging.Client().logger("logger_name")
#   logger.log_text(whatever_variable_or_text)
def respond_to_trigger(req):
    creds = authenticate()
    service = create_service('gmail', 'v1', creds)
    user_info = service.users().getProfile(userId='me').execute()
    the_sender = user_info["emailAddress"]
    the_recipient = "tailrusse2020@gmail.com"
    the_subject = "testing again again and again"
    the_text = "You should see this when I select a file"
    the_message = create_message(the_sender, the_recipient, the_subject, the_text)
    send_message(service, "me", the_message)
    request_json = req.get_json(silent=True)
    selected_itmes = request_json["drive"]["selectedItems"]
    first_item = selected_itmes[0]
    return create_card(first_item["title"], first_item["iconUrl"])

import base64
import json
from email.mime.text import MIMEText
from googleapiclient import errors
from googleapiclient.discovery import build
from Backend import authorization
from google.cloud import datastore
import Backend.datastoreMethods as dataMethods


def create_service(addon_name, version):
    cred = authorization.authenticate()
    service = build(addon_name, version, credentials=cred)
    return service, cred


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


def file_list_response(page_token=0):
    drive_service, _ = create_service("drive", "v3")
    if page_token == 0:
        response = drive_service.files().list().execute()
    else:
        response = drive_service.files().list(pageToken=page_token).execute()

    return response


def create_list_items(files):
    file_list = []
    # response = file_list_response()
    file_list.extend(files)
    list_items = []
    for file in file_list:
        file_to_add = {
            "text": file['name'],
            "value": json.dumps(file)
            # "selected": True
        }
        list_items.append(file_to_add)
    return json.dumps(list_items)


def get_recent_changes():
    drive_service, cred = create_service("drive", "v3")
    current_page_token = drive_service.changes().getStartPageToken().execute()
    page_token = int(current_page_token["startPageToken"]) - 1
    changes = drive_service.changes().list(pageToken=page_token).execute()
    return changes


def respond_to_trigger(req):
    service, _ = create_service('gmail', 'v1')
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

# To get all changes
# changes = drive_service.changes().list(pageToken=1).execute()
# is_valid = True
# if 'nextPageToken' not in changes:
#     is_valid = False
#
# while is_valid:
#     if 'nextPageToken' not in changes:
#         is_valid = False
#         print(int(changes['newStartPageToken']))
#     else:
#         next_page_token_int = int(changes['nextPageToken'])
#         print(next_page_token_int)
#         changes = drive_service.changes().list(pageToken=next_page_token_int).execute()

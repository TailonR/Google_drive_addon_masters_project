import base64
from email.mime.text import MIMEText
from googleapiclient import errors
from googleapiclient.discovery import build
from Backend import authorization


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
def create_message(source, to, subject, message_text):
    message = MIMEText(message_text)
    message['from'] = source
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
def send_message(user_id, message):
    gmail_service, _ = create_service('gmail', 'v1')
    try:
        message = (gmail_service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def file_list_response(query, page_token=0):
    drive_service, _ = create_service("drive", "v3")
    if page_token == 0:
        response = drive_service.files().list(q=query).execute()
    else:
        response = drive_service.files().list(q=query, pageToken=page_token).execute()

    return response


def get_recent_changes():
    drive_service, _ = create_service("drive", "v3")
    current_page_token = drive_service.changes().getStartPageToken().execute()
    page_token = int(current_page_token["startPageToken"]) - 1
    changes = drive_service.changes().list(pageToken=page_token).execute()
    return changes


def get_file_fields(file_id, field):
    drive_service, _ = create_service("drive", "v3")
    response = drive_service.files().get(fileId=file_id, fields=field).execute()
    return response

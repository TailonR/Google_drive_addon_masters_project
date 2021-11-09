import base64
from email.mime.text import MIMEText
from googleapiclient import errors
from googleapiclient.discovery import build


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

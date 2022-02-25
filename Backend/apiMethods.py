import base64
from email.mime.text import MIMEText
from googleapiclient import errors
from googleapiclient.discovery import build
from Backend import authorization
from Backend import datastoreMethods

# Create a Python representation the given api.
#
# Args:
#   api_name: name of the api to build.
#   version: the version of the api to build.
#
# Returns:
#   The Python api representation.
#   The credentials used to authenticate the addon (used for creating channels).
def create_service(api_name, version):
    cred = authorization.authenticate()
    service = build(api_name, version, credentials=cred)
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
        print('Message Id:', message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


# Get a list of files matching the query.
#
# Args:
#   query: The query for matching specific files.
#   page_token: the token for a specific page of results.
#
# Returns:
#   The results of the query.
def file_list_response(query, page_token=0):
    drive_service, _ = create_service("drive", "v3")
    if page_token == 0:
        response = drive_service.files().list(q=query).execute()
    else:
        response = drive_service.files().list(q=query, pageToken=page_token).execute()

    return response


# Get the recent changes.
#
# Args:
#   page_token: the token to get the page of results.
#
# Returns:
#   The list of changes.
def get_recent_changes():
    drive_service, _ = create_service("drive", "v3")
    previous_page_token = datastoreMethods.get_start_page_token()
    changes = drive_service.changes().list(pageToken=previous_page_token["previousPageToken"]).execute()
    datastoreMethods.store_start_page_tokens(changes["newStartPageToken"])
    return changes


# Get the field of a specific file.
#
# Args:
#   file_id: The id of the specific file.
#   field: The field requested.
#
# Returns:
#   The field of the file indicated.
def get_file_fields(file_id, field):
    drive_service, _ = create_service("drive", "v3")
    response = drive_service.files().get(fileId=file_id, fields=field).execute()
    return response

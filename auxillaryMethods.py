import json
import Backend.datastoreMethods as datastoreMethods
import Backend.apiMethods as Methods


# Get the input values of the request.
#
# Args:
#   form_submit_response: the form submit response.
#   containing the desired information.
#
# Returns:
#   The value of the string inputs (the selected files).
def get_string_input_values(form_submit_response):
    return form_submit_response["commonEventObject"]["formInputs"]["Selection Input"]["stringInputs"]["value"]


# Add text widgets to the given card.
# The text widgets will contain the names
# of the selected items.
#
# Args:
#   selected_items: the selected items.
#   given_card: the card to add the widgets to.
def add_text_widgets(selected_items, given_card):
    for selected_item in selected_items:
        loaded_json = json.loads(selected_item)
        widget_item = {}
        if "name" in loaded_json:
            widget_item = {
                "text": loaded_json["name"]
            }
        elif "title" in loaded_json:
            widget_item = {
                "text": loaded_json["title"]
            }

        given_card.add_widget("textParagraph", widget_item)


# Create list items for the list card.
#
# Args:
#   files: The files to make the list out of.
#
# Returns:
#   A json representation of a list of the given files.
def create_list_items(files):
    file_list = []
    file_list.extend(files)
    list_items = []
    for file in file_list:
        # check if the file already
        # is being tracked
        file_to_add = {
            "text": file['name'],
            "value": json.dumps(file)
            # "selected": True
        }
        list_items.append(file_to_add)
    return json.dumps(list_items)


# Create a json representation of the "add email" button.
#
# Args:
#   card_json: The json representation of the
#   card to add the email button to.
#   text_input: the json representation of the
#   text input widget to be added in the next card.
#
# Returns:
#   A json representation of the "add email" button.
def build_add_email_button(card_json, text_input):
    return {
        "text": "+Add Email",
        "disabled": False,
        "color": {
            "red": 0.32421,
            "blue": 0.23421,
            "green": 0.2353614
        },
        "onClick": {
            "action": {
                "function": "https://helloworld-s2377xozpq-uc.a.run.app/add-email",
                "parameters": [
                    {
                        "key": "card",
                        "value": json.dumps(card_json)
                    },
                    {
                        "key": "textInput",
                        "value": json.dumps(text_input)
                    }
                ],
                "persistValues": True
            }
        }
    }


# Get the emails from the form input.
#
# Args:
#   form_input: The form input containing the emails.
#
# Returns:
#   A list of the emails in the form input
def get_emails(form_inputs):
    emails = []
    for key, value in form_inputs.items():
        if isinstance(value, dict):
            emails.extend(get_emails(value))
        else:
            emails.append(value[0])
    return emails


# Get the given property of the given files.
#
# Args:
#   file_json: The json representation of a list of files.
#   attribute: The property of the files to search for.
#
# Returns:
#   A list of the value of the given property in each file.
def get_file_property(file_json, attribute):
    file_attributes = []
    for file in file_json:
        file_loaded = json.loads(file)
        for key, value in file_loaded.items():
            if key == attribute:
                file_attributes.append(value)
    return file_attributes


# Send a message for each file to every email associated with it.
#
# Args:
#   files: The files to send an email about their changes.
#   parent_id: The id of a folder. Given if a file change occurs
#   on a file that is inside a folder being tracked. (optional).
def send_message(files, parent_id=""):
    gmail_service, _ = Methods.create_service('gmail', 'v1')
    user_info = gmail_service.users().getProfile(userId='me').execute()
    source = user_info["emailAddress"]
    for file in files:
        file_id = file["fileId"]
        emails: []
        if parent_id == "":
            emails = datastoreMethods.get_emails(file_id)
        else:
            emails = datastoreMethods.get_emails(parent_id)

        subject = f"{file['file']['name']} has been updated"
        for email in emails:
            recipient = email
            name = recipient[0:5]
            text = f"Hello {name}, \nIf you are seeing this, then a file had been edited"
            email_bytes = Methods.create_message(source, recipient, subject, text)
            Methods.send_message("me", email_bytes)


# Filters the given items into a list of folders
# and a list of files.
#
# Args:
#   files: The files to filter.
#
# Returns:
#   A list of folders and a list of files
def filter_items(files):
    folder_list = []
    file_list = []
    for file in files:
        if file["mimeType"] == "application/vnd.google-apps.folder":
            folder_list.append(file)
        else:
            file_list.append(file)

    return folder_list, file_list

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
def add_text_widgets(selected_items, card):
    for selected_item in selected_items:
        widget_item = {}
        if "name" in selected_item:
            widget_item = {
                "text": selected_item["name"]
            }
        elif "title" in selected_item:
            widget_item = {
                "text": selected_item["title"]
            }

        card.add_widget("textParagraph", widget_item)


# Get the file_ids that are being tracked.
# Helps with the list card
def get_all_file_ids_tracked():
    files_info = datastoreMethods.get_tracked_file_info()
    if files_info is None:
        return None
    file_ids_for_emails = []
    for info in files_info:
        file_ids_for_emails.append(info.key.id_or_name)
    return file_ids_for_emails


# Create list items for the list card.
#
# Args:
#   files: The files to make the list out of.
#
# Returns:
#   A json representation of a list of the given files.
def create_list_items_for_list_card(files):
    file_list = []
    file_list.extend(files)
    list_items = []
    for file in file_list:
        # check if the file already is being tracked
        file_to_add = {
            "text": file['name'],
            "value": json.dumps(file),
        }
        list_items.append(file_to_add)
    return list_items


# Create list items for the stop tracking card.
#
# Args:
#   files: The files to make the list out of.
#
# Returns:
#   A json representation of a list of the given files.
def create_list_items_for_stop_tracking_card(tracked_file_info):
    list_items = []
    for file_info in tracked_file_info:
        # check if the file already is being tracked
        file_to_add = {
            "text": file_info["fileName"],
            "value": file_info.key.id_or_name,
        }
        list_items.append(file_to_add)
    return list_items


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
        for key, value in file.items():
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
            emails = datastoreMethods.get_tracked_file_info(file_id, "emails")
        else:
            emails = datastoreMethods.get_tracked_file_info(parent_id, "emails")

        subject = f"{file['file']['name']} has been updated"
        for email in emails:
            name = email[0:5]
            text = f"Hello {name}, \nIf you are seeing this, then a file had been edited"
            email_bytes = Methods.create_message(source, email, subject, text)
            Methods.send_message("me", email_bytes)

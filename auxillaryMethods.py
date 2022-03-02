import json
import Backend.datastoreMethods as datastoreMethods
import Backend.apiMethods as Methods
from datetime import datetime
import pytz


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
# of the selected items and will be displayed
# on the item tracking card.
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
def get_emails_from_form_input(form_inputs):
    emails = []
    for key, value in form_inputs.items():
        if isinstance(value, dict):
            emails.extend(get_emails_from_form_input(value))
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


# Deliver a message for each file to every email associated with it.
#
# Args:
#   files: The files to send an email about their changes.
#   parent_id: The id of a folder. Given if a file change occurs
#   on a file that is inside a folder being tracked. (optional).
def deliver_message(id_and_name, subject, message_text, parent_id=""):
    gmail_service, _ = Methods.create_service('gmail', 'v1')
    user_info = gmail_service.users().getProfile(userId='me').execute()
    source = user_info["emailAddress"]
    file_id = id_and_name[0]
    emails: []
    if parent_id == "":
        emails = datastoreMethods.get_tracked_file_info(file_id, "emails")
    else:
        emails = datastoreMethods.get_tracked_file_info(parent_id, "emails")

    for email in emails:
        email_bytes = Methods.create_message(source, email, subject, message_text)
        Methods.send_message("me", email_bytes)


# Determine if the file was created or uploaded recently.
#
# In order for this to work, the UTC time must be converted
# to the local time of the user.
#
# Args:
#   creation_date_string: the date of creation in a string format. In UTC time.
#
# Returns:
#   true if the time since the file was created is less than 30 seconds
#   false if otherwise.
def is_added(creation_date_string):
    time_format = "%Y-%m-%dT%H:%M:%S.%fz"
    created_time = datetime.strptime(creation_date_string, time_format)
    local_time = pytz.utc.localize(created_time, is_dst=None).astimezone()
    time_since_creation = datetime.now().astimezone() - local_time
    return time_since_creation.total_seconds() < 30


# Determine if an ancestor of the file is being tracked (this includes parents).
#
# Args:
#   file_id: The id of the file whose parents will be checked to see if they
#   are tracked.
#
# Returns:
#   The file_id of the tracked ancestor, if one exists.
#   If no ancestor is tracked, None.
def check_ancestors(file_id):
    response = Methods.get_file_fields(file_id, "parents")
    if "parents" not in response:
        return None
    for parent_id in response["parents"]:
        if datastoreMethods.get_tracked_file_info(parent_id) is not None:
            return parent_id
        else:
            return check_ancestors(parent_id)
    return None

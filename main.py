import json
import os
import uuid
import cards
from card import Card
from flask import Flask, request
from Backend import apiMethods as Methods
from Backend import channel
import auxillaryMethods as auxMethods
from google.cloud import storage
from googleapiclient import errors
import Backend.datastoreMethods as datastoreMethods

# See if you even need the credentials

app = Flask(__name__)


# methods=['GET', 'POST', 'DELETE']   Possible methods

@app.route("/", methods=['POST'])
# Creates a card with two widgets.
def load_homepage():
    # Need to store channel information so that
    # channel for changes can be created for
    # new file tracking
    # ======== Uncomment line below ===========
    return cards.homepage_card()


@app.route("/more-items", methods=['POST'])
# Creates a card with two widgets.
def get_more_items():
    req_json = request.get_json(silent=True)
    next_page_token = req_json["commonEventObject"]["parameters"]["nextPageToken"]
    called_by = req_json["commonEventObject"]["parameters"]["from"]  # could have another parameter, that is the index
    card: Card                                                       # of the max-limited response (If the response
    if called_by == "folder":                                        # gives me more results than the max limit)
        card = cards.list_card(False, next_page_token)
    else:
        card = cards.list_card(True, next_page_token)

    return card.push_card()


@app.route("/go-back", methods=['POST'])
# Creates a card with two widgets.
def go_back():
    return {
        "renderActions": {
            "action": {
                "navigations": [
                    {
                        "pop": True
                    }
                ]
            }
        }
    }


@app.route("/item-selected", methods=['POST'])
def item_selected():
    req_json = request.get_json(silent=True)
    selected_items = req_json["drive"]["selectedItems"]
    selected_items_string = []
    for selected_item in selected_items:
        selected_items_string.append(json.dumps(selected_item))
    card = cards.item_to_be_tracked_card(selected_items_string)
    return card.display_card()


@app.route("/trigger", methods=['POST'])
def trigger():
    changes = Methods.get_recent_changes()
    print(f"The changes: {changes}")
    # Send emails
    auxMethods.send_message(changes["changes"])
    return cards.notification_card("")


# Here is where we create channels for the children if the file type is a folder
@app.route("/track-item", methods=['POST'])
def track_item():
    # get the request payload
    req_json = request.get_json(silent=True)
    if "formInputs" not in req_json["commonEventObject"]:
        return cards.notification_card("No emails were provided")
    else:
        form_inputs = req_json["commonEventObject"]["formInputs"]
        emails = auxMethods.get_emails(form_inputs)

    # get the json for the selected files
    files = req_json["commonEventObject"]["parameters"]["selectedFiles"]
    # create a list of the file names
    file_names = auxMethods.get_file_attribute(json.loads(files), "name")
    # create a list of the file ids
    file_ids = auxMethods.get_file_attribute(json.loads(files), "id")
    datastoreMethods.store_emails(file_ids, emails)
    # ========================================
    # Here is where we could loop through the files, if there are files with the mimeType of
    # 'application/vnd.google-apps.folder' we will run file_list_response with a query for all
    # files with parents that have the file_id of that folder and then create channels for them

    files_loaded = json.loads(files)
    child_file_ids = []
    for file in files_loaded:
        file_loaded = json.loads(file)
        if file_loaded["mimeType"] == "application/vnd.google-apps.folder":
            channel.create_channel_changes()
            response = Methods.file_list_response(f"'{file_loaded['id']}' in parents")
            files_in_folder = response["files"]
            child_file_ids = [file["id"] for file in files_in_folder]
            datastoreMethods.store_emails(child_file_ids, emails)

    # ====================================

    # create channels
    try:
        auxMethods.create_channels(file_ids)  # creates channels for selected files; could make this
        if len(child_file_ids) > 0:             # create_multiple_channels and have it in channel
            auxMethods.create_channels(child_file_ids)  # creates channels for children if folder was selected;
    except errors.HttpError as error:             # could make this create_multiple_channels and have it in channel
        message = f"An error occurred: {error}"
        return cards.notification_card(message)

    # return notification card
    comma_delimiter = ", "
    message = f"{comma_delimiter.join(file_names)} are tracked"
    return cards.notification_card(message)


@app.route("/add-email", methods=['POST'])
def add_email():
    req_json = request.get_json(silent=True)
    card_string = req_json["commonEventObject"]["parameters"]["card"]
    card_json = json.loads(card_string)
    copy_of_card = Card(card_json)
    input_name = str(uuid.uuid4())
    text_input = {
        "name": f"Email {input_name}",
        "label": "Enter Email",
        "value": "",
    }
    copy_of_card.add_widget("textInput", text_input)
    button_list = {
        "buttons": [
            auxMethods.build_add_email_button(copy_of_card.get_card(), text_input)
        ]
    }
    copy_of_card.add_widget("buttonList", button_list)
    return copy_of_card.replace_card()


# What if a user selects a folder to track?
# This is gonna require us to do some things:
#   1) We need to monitor files being created in a folder
#   2) We then need to create channels for each file underneath
#       a folder
#   ========================================================
# I'm thinking the way we do this is that when ever a user selects a folder
# then all the child files will have channels created for them
# 1) When there are files in the folder
#   - query for all the files that contain the folder id as a parent
#   - then create channels with the files returned in the response
# 2) When a new file is added to the folder
#   - Monitor for all changes so we are notified when a new file is added
#   - Check if that new file has the correct parent id
#   - if so create a channel for it
@app.route("/file-to-be-tracked", methods=['POST'])
def item_to_be_tracked():
    req_json = request.get_json(silent=True)
    selected_files = auxMethods.get_string_input_values(req_json)
    card = cards.item_to_be_tracked_card(selected_files)
    return card.push_card()


# The route that push notifications on changes are going to be directed to
# Since we are monitoring for all changes, if there is a on an old file
# this function will also be called, so we need to only proceed if the
# file is new
@app.route("/new-file-added", methods=['POST'])
def handle_new_file_notification():
    changes = Methods.get_recent_changes()
    drive_service, _ = Methods.create_service("drive", "v3")
    for file in changes["changes"]:
        file_id = file["fileId"]
        response = drive_service.files().get(fileId=file_id, fields="parents").execute()
        for parent_id in response["parents"]:
            # make a call to datastore to figure out if the parent_id matches any we have to keep track of
            # This means we need to store parent ids in the datastore
            channel_entity = datastoreMethods.get_channel_info(parent_id)
            if channel_entity is not None:
                # Send emails
                auxMethods.send_message([file], parent_id)
    return cards.notification_card("")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    # Maybe create the credentials here so that they can be passed around
    # Here a (probably static) class will be initialized
    # This class will be responsible for maintaining the credentials

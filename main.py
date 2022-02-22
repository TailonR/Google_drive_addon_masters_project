import json
import os
import cards
import time
from card import Card
from flask import Flask, request
from Backend import apiMethods as Methods
from Backend import channel
import auxillaryMethods as auxMethods
from googleapiclient import errors
import Backend.datastoreMethods as datastoreMethods
import Backend.authorization as authorization

app = Flask(__name__)


# Push the homepage to the card stack.
#
# Returns:
#   The json representation of the homepage card.
@app.route("/", methods=['POST'])
# Creates a card with two widgets.
def load_homepage():
    return cards.homepage_card()


# Push the card to the card stack.
# The function gets the request used when calling the path and uses that information
# to find a new list of results and use those in the card.
@app.route("/more-items", methods=['POST'])
def get_more_items():
    req_json = request.get_json(silent=True)
    next_page_token = req_json["commonEventObject"]["parameters"]["nextPageToken"]
    called_by = req_json["commonEventObject"]["parameters"]["from"]  # could have another parameter, that is the index
    card: Card  # of the max-limited response (If the response
    if called_by == "folder":  # gives me more results than the max limit)
        card = cards.list_card(False, next_page_token)
    else:
        card = cards.list_card(True, next_page_token)

    return card.push_card()


# Returns the instructions to pop the card created after clicking the "more items" button.
# Returns:
#   The json representation of the instructions to pop the top card in the stack.
@app.route("/go-back", methods=['POST'])
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


# Push the item tracking card to the card stack.
# The function gets the request used to call the path and creates the
# item tracking card based on the files selected.
# Returns:
#   The json representation of the item tracking card.
@app.route("/item-selected", methods=['POST'])
def item_selected():
    req_json = request.get_json(silent=True)
    selected_items = req_json["drive"]["selectedItems"]
    card = cards.item_tracking_card(selected_items)
    return card.display_card()


# Gets the most recent changes and sends messages to the correct emails.
#
# Returns:
#   The notification card.
@app.route("/trigger", methods=['POST'])
def trigger():
    changes = Methods.get_recent_changes()
    file_ids = [file["fileId"] for file in changes["changes"]]
    # Send messages to the correct emails, if any.
    for file_id in file_ids:
        # Send messages for the check-marked files.
        if datastoreMethods.get_tracked_file_info(file_id) is not None:
            auxMethods.send_message(changes["changes"])
        else:
            # Send messages for the check-marked folders.
            response = Methods.get_file_fields(file_id, "parents")
            for parent_id in response["parents"]:
                if datastoreMethods.get_tracked_file_info(parent_id) is not None:
                    auxMethods.send_message(changes["changes"], parent_id)
    return cards.notification_card("")


# Store the emails given for the check-marked files and create a channel.
# This functions uses the request used when calling the function to get the
# provided emails and the check-marked files or folders.
#
# Returns:
#   A notification card containing the message that the selected files are tracked.
@app.route("/track-item", methods=['POST'])
def track_item():
    req_json = request.get_json(silent=True)
    emails: []
    # Determine if emails were provided.
    if "formInputs" not in req_json["commonEventObject"]:
        return cards.notification_card("No emails were provided")
    else:
        form_inputs = req_json["commonEventObject"]["formInputs"]
        emails = auxMethods.get_emails(form_inputs)

    # Create a channel for change notifications
    try:
        # Only create a channel if none exists already
        channel_entity = datastoreMethods.get_channel_info()
        curr_time_ms = round(time.time() * 1000)
        if channel_entity is None or int(channel_entity["expiration"]) < curr_time_ms:
            channel.create_channel()
    except errors.HttpError as error:
        message = f"An error occurred: {error}"
        return cards.notification_card(message)
    # Get the json representation for the selected files.
    files = json.loads(req_json["commonEventObject"]["parameters"]["selectedFiles"])

    # Get the file_ids for the check-marked file, or if the file is a folder,
    # the file_ids of the files inside the folder, and store them in the datastore
    for file in files:
        if "name" in file:
            datastoreMethods.store_file_info(file["id"], file["name"], emails)
        elif "title" in file:
            datastoreMethods.store_file_info(file["id"], file["title"], emails)

    # Return a notification card
    file_names = []
    if "name" in files[0]:
        file_names = auxMethods.get_file_property(files, "name")
    elif "title" in files[0]:
        file_names = auxMethods.get_file_property(files, "title")
    comma_delimiter = ", "
    message = f"{comma_delimiter.join(file_names)} {'are' if len(file_names) > 1 else 'is'} tracked"
    return cards.notification_card(message)


# Add a text input widget so the user can add another email
#
# Returns:
#   The json representation of a card containing an extra email input field.
@app.route("/add-email", methods=['POST'])
def add_email():
    req_json = request.get_json(silent=True)
    previous_email_inputs = json.loads(req_json["commonEventObject"]["parameters"]["previousEmailInputs"])
    selected_files = json.loads(req_json["commonEventObject"]["parameters"]["selectedFiles"])
    card = cards.item_tracking_card(selected_files, previous_email_inputs)
    return card.replace_card()


# Create the item tracking card.
#
# Returns:
#   The json representation of the file tracking card.
@app.route("/file-tracking", methods=['POST'])
def item_tracking():
    req_json = request.get_json(silent=True)
    selected_files = auxMethods.get_string_input_values(req_json)
    for index in range(0, len(selected_files)):
        selected_files[index] = json.loads(selected_files[index])
    card = cards.item_tracking_card(selected_files)
    return card.push_card()


# Create the stop tracking card.
#
# Returns:
#   The json representation of the stop tracking card.
@app.route("/stop-tracking", methods=['POST'])
def stop_tracking():
    tracked_files_info = datastoreMethods.get_tracked_file_info()
    card = cards.stop_tracking_card(tracked_files_info)
    return card.push_card()


# Deletes tracking information for the selected files
@app.route("/end-tracking", methods=['POST'])
def end_tracking():
    req_json = request.get_json(silent=True)
    selected_file_ids: []
    if "formInputs" in req_json:
        selected_file_ids = auxMethods.get_string_input_values(req_json)
    else:
        selected_files = json.loads(req_json["commonEventObject"]["parameters"]["selectedFiles"])
        selected_file_ids = [file["id"] for file in selected_files]

    file_entities = datastoreMethods.get_tracked_file_info()
    for entity in file_entities:
        if entity.key.id_or_name in selected_file_ids:
            datastoreMethods.delete_datastore_entity("TrackedFiles", entity.key.id_or_name)
        if len(datastoreMethods.get_tracked_file_info()) == 0:
            channel.stop_channel()
    if len(file_entities) > 0:
        return cards.notification_card("The selected files are no longer being tracked")
    else:
        return cards.notification_card("The selected Files are not being tracked")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    if not datastoreMethods.token_exists():
        authorization.authenticate()

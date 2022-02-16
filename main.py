import json
import os
import uuid
import cards
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
    card: Card                                                       # of the max-limited response (If the response
    if called_by == "folder":                                        # gives me more results than the max limit)
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
    selected_items_string = []
    for selected_item in selected_items:
        selected_items_string.append(json.dumps(selected_item))
    card = cards.item_tracking_card(selected_items_string)
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
        if datastoreMethods.get_emails(file_id) is not None:
            auxMethods.send_message(changes["changes"])
        else:
            # Send messages for the check-marked folders.
            response = Methods.get_file_fields(file_id, "parents")
            for parent_id in response["parents"]:
                if datastoreMethods.get_emails(parent_id) is not None:
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

    # Get the json representation for the selected files.
    files = req_json["commonEventObject"]["parameters"]["selectedFiles"]

    # Get the file_ids for the check-marked file, or if the file is a folder,
    # the file_ids of the files inside the folder, and store them in the datastore
    for file in json.loads(files):
        file_loaded = json.loads(file)
        if file_loaded["mimeType"] == "application/vnd.google-apps.folder":
            response = Methods.file_list_response(f"'{file_loaded['id']}' in parents")
            child_file_ids = [file["id"] for file in response["files"]]
            datastoreMethods.store_emails([file_loaded["id"]], emails)
            datastoreMethods.store_emails(child_file_ids, emails)
        else:
            datastoreMethods.store_emails(file_loaded["id"], emails)

    try:
        # Only create a channel if none exists already
        if datastoreMethods.get_channel_info() is None:
            channel.create_channel()
    except errors.HttpError as error:
        message = f"An error occurred: {error}"
        return cards.notification_card(message)

    # Return a notification card
    file_names = auxMethods.get_file_property(json.loads(files), "name")
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
    # Get the json representation of card
    card_string = req_json["commonEventObject"]["parameters"]["card"]
    card_json = json.loads(card_string)
    # Create a new card based on the json of the old one
    copy_of_card = Card(card_json)
    input_name = str(uuid.uuid4())
    text_input = {
        "name": f"Email {input_name}",
        "label": "Enter Email",
        "value": "",
    }
    # Add a new text input widget along with a "add email" button
    copy_of_card.add_widget("textInput", text_input)
    button_list = {
        "buttons": [
            auxMethods.build_add_email_button(copy_of_card.get_card(), text_input)
        ]
    }
    copy_of_card.add_widget("buttonList", button_list)
    return copy_of_card.replace_card()


# Create the item tracking card.
#
# Returns:
#   The json representation of the file tracking card.
@app.route("/file-tracking", methods=['POST'])
def item_tracking():
    req_json = request.get_json(silent=True)
    selected_files = auxMethods.get_string_input_values(req_json)
    card = cards.item_tracking_card(selected_files)
    return card.push_card()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    if not datastoreMethods.token_exists():
        authorization.authenticate()

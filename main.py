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
    return cards.homepage_card()


@app.route("/more-items", methods=['POST'])
# Creates a card with two widgets.
def get_more_items():
    req_json = request.get_json(silent=True)
    next_page_token = req_json["commonEventObject"]["parameters"]["nextPageToken"]
    homepage_card = cards.homepage_card(next_page_token)
    return {
        "renderActions": json.loads(homepage_card)
    }


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
    req_json = request.get_json()
    selected_items = req_json["drive"]["selectedItems"]
    return cards.item_selected_card(selected_items)


@app.route("/trigger", methods=['POST'])
def trigger():
    req_json = request.get_json(silent=True)
    changes = Methods.get_recent_changes()
    print(f"The changes: {changes}")
    # Send emails
    gmail_service, _ = Methods.create_service('gmail', 'v1')
    user_info = gmail_service.users().getProfile(userId='me').execute()
    source = user_info["emailAddress"]
    auxMethods.send_message(changes["changes"], gmail_service, source)
    return cards.notification_card("")


@app.route("/track-item", methods=['POST'])
def track_item():
    # get the request payload
    req_json = request.get_json(silent=True)
    # get the json for the selected files
    files = req_json["commonEventObject"]["parameters"]["selected_files"]
    # create a list of the file names
    file_names = auxMethods.get_file_attribute(json.loads(files), "name")
    # create a list of the file ids
    file_ids = auxMethods.get_file_attribute(json.loads(files), "id")
    # create channels
    try:
        auxMethods.create_channels(file_ids)
    except errors.HttpError as error:
        message = f"An error occurred: {error}"
        return cards.notification_card(message)

    # get the json for the given emails
    form_inputs = req_json["commonEventObject"]["formInputs"]
    emails = auxMethods.get_emails(form_inputs)
    datastoreMethods.store_emails(file_ids, emails)
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
    return copy_of_card.push_card()


@app.route("/file-to-be-tracked", methods=['POST'])
def item_to_be_tracked():
    req_json = request.get_json(silent=True)
    selected_files = auxMethods.get_string_input_values(req_json)
    return cards.item_to_be_tracked_card(selected_files)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    # Maybe create the credentials here so that they can be passed around
    # Here a (probably static) class will be initialized
    # This class will be responsible for maintaining the credentials

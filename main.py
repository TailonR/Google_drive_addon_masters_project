import os
import cards
from flask import Flask, request
from Backend import apiMethods as Methods
from Backend import channel
import auxillaryMethods as auxMethods

app = Flask(__name__)


# methods=['GET', 'POST', 'DELETE']   Possible methods

@app.route("/", methods=['POST'])
# Creates a card with two widgets.
def load_homepage():
    return cards.homepage_card()


@app.route("/item-selected", methods=['POST'])
def item_selected():
    req_json = request.get_json()
    selected_items = req_json["drive"]["selectedItems"]
    return cards.item_selected_card(selected_items)


@app.route("/create-channel", methods=['POST'])
def create_channel():
    req_json = request.get_json(silent=True)
    event_object = req_json["commonEventObject"]
    if "formInputs" in event_object:
        input_values = auxMethods.get_string_input_values(req_json)
        item_name = auxMethods.get_item_name(input_values[0])
        file_id = ""
        files = Methods.get_files()
        for file in files:
            if file['name'] == item_name:
                file_id = file['id']
        channel.dev_create_channel(file_id)
        return cards.notification_card(item_name)
    return cards.notification_card("")


@app.route("/trigger", methods=['POST'])
def trigger():
    changes = Methods.get_recent_changes()
    print(changes)
    return cards.homepage_card()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

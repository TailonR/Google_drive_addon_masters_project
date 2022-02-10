import json
import Backend.channel as channel
from googleapiclient import errors
import Backend.datastoreMethods as datastoreMethods
import Backend.apiMethods as Methods


def get_item_name(input_value):
    input_value = input_value.replace("Selection Input", "")
    input_value = input_value.replace("Value", "")
    input_value = input_value.strip()
    return input_value


def get_string_input_values(form_submit_response):
    return form_submit_response["commonEventObject"]["formInputs"]["Selection Input"]["stringInputs"]["value"]


def add_widgets(selected_items, given_card):
    for selected_item in selected_items:
        loaded_json = json.loads(selected_item)
        widget_item = {
            "text": loaded_json["name"]
        }
        given_card.add_widget("textParagraph", widget_item)


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


def get_emails(form_inputs):
    emails = []
    for key, value in form_inputs.items():
        if isinstance(value, dict):
            emails.extend(get_emails(value))
        else:
            emails.append(value[0])
    return emails


def get_file_attribute(file_json, attribute):
    file_attributes = []
    for file in file_json:
        file_loaded = json.loads(file)
        for key, value in file_loaded.items():
            if key == attribute:
                file_attributes.append(value)
    return file_attributes


def create_channels(file_ids):
    try:
        for fid in file_ids:
            channel.dev_create_channel(fid)
    except errors.HttpError as error:
        raise error


def send_message(files, service, source):
    for file in files:
        file_id = file["fileId"]
        emails = datastoreMethods.get_emails(file_id)
        subject = f"{file['file']['name']} has been updated"
        for email in emails:
            recipient = email
            name = recipient[0:5]
            text = f"Hello {name}, \nIf you are seeing this, then a file had been edited"
            email_bytes = Methods.create_message(source, recipient, subject, text)
            Methods.send_message(service, "me", email_bytes)


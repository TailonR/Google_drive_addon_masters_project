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


def create_list_items(files):
    file_list = []
    file_list.extend(files)
    list_items = []
    for file in file_list:
        file_to_add = {
            "text": file['name'],
            "value": json.dumps(file)
            # "selected": True
        }
        list_items.append(file_to_add)
    return json.dumps(list_items)


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
            channel.create_channel(fid)
    except errors.HttpError as error:
        raise error


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


def filter_items(files):
    folder_list = []
    file_list = []
    for file in files:
        if file["mimeType"] == "application/vnd.google-apps.folder":
            folder_list.append(file)
        else:
            file_list.append(file)

    return folder_list, file_list

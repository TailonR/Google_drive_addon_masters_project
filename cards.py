import json
from Backend import apiMethods as Methods
import auxillaryMethods as auxMethods
from Backend import authorization
from card import Card
import uuid


def homepage_card(page_token=0):
    folder_card = list_card(False, page_token)
    file_card = list_card(True, page_token)

    decorated_text_folders = {
        "topLabel": "Select Folders",
        "text": "Select folders to track",
        "onClick": {
            "card": folder_card.get_card()
        }
    }
    decorated_text_files = {
        "topLabel": "Select Files",
        "text": "Select Files to track",
        "onClick": {
            "card": file_card.get_card()
        }
    }

    home_card = Card("Main Card")
    home_card.create_card("Files or Folders to track")
    home_card.update_action()
    home_card.add_section("Go to Folders or Files", False)
    home_card.add_widget("decoratedText", decorated_text_folders)
    home_card.add_widget("decoratedText", decorated_text_files)
    return home_card.display_card()


# This function takes a file flag which is a bool that determines if we are creating
# a card for a list of files or a list of folders.
# It'll take a page token so that it knows which page of results to get
def list_card(file_flag, page_token):
    item_list_card = Card(f"{'Files' if file_flag else 'Folders'} Card")
    if file_flag:
        response = Methods.file_list_response("mimeType!='application/vnd.google-apps.folder'", page_token)
    else:
        response = Methods.file_list_response("mimeType='application/vnd.google-apps.folder'", page_token)

    next_page_token = response["nextPageToken"] if "nextPageToken" in response else -1
    tuple_of_folders_and_files = auxMethods.filter_items(response["files"])
    items = tuple_of_folders_and_files[file_flag]  # the items will either folders or files depending on the flag
    fixed_footer = {
        "primaryButton": {
            "text": "Next",
            "color": {
                "red": 0,
                "blue": 0,
                "green": 0
            },
            "onClick": {
                "action": {
                    "function": "https://helloworld-s2377xozpq-uc.a.run.app/file-tracking",
                }
            }
        },
        "secondaryButton": {
            "text": "Does nothing",
            "color": {
                "red": 0,
                "blue": 0,
                "green": 0
            },
            "disabled": True,
            "onClick": {
                "openLink": {
                    "url": "www.google.com",
                    "onClose": "NOTHING",  # Change this
                    "openAs": "OVERLAY"
                }
            }
        }
    }
    button = {
        "buttons": [
            {
                "color": {
                    "red": 0,
                    "blue": 0,
                    "green": 0
                },
                "disabled": True if page_token == 0 else False,
                "onClick": {
                    "action": {
                        "function": "https://helloworld-s2377xozpq-uc.a.run.app/go-back"
                    }
                },
                "text": "back"
            },
            {
                "color": {
                    "red": 0.32421,
                    "blue": 0.23421,
                    "green": 0.2353614
                },
                "disabled": False if next_page_token != -1 else True,
                "onClick": {
                    "action": {
                        "function": "https://helloworld-s2377xozpq-uc.a.run.app/more-items",
                        "parameters": [
                            {
                                "key": "nextPageToken",
                                "value": next_page_token
                            },
                            {
                                "key": "from",
                                "value": f"{'file' if file_flag else 'folder'}"
                            }
                        ]
                    }
                },
                "text": "more"
            }
        ]
    }
    selection_input_item = {
        "name": "Selection Input",
        "label": "Selection Input",
        "type": "CHECK_BOX",
        "items": json.loads(auxMethods.create_list_items(items)),
    }
    item_list_card.update_action()
    item_list_card.create_card(f"{'Files' if file_flag else 'Folders'} to Watch", fixed_footer)
    item_list_card.add_section(f"Select {'Files' if file_flag else 'Folders'}", False)
    item_list_card.add_widget("selectionInput", selection_input_item)
    item_list_card.add_widget("buttonList", button)
    return item_list_card


def item_tracking_card(selected_files):
    card = Card("Notifications")
    email_attribute_name = str(uuid.uuid4())
    text_input = {
        "name": f"Email {email_attribute_name}",
        "label": "Enter Email",
        "value": "",
    }
    fixed_footer = {
        "primaryButton": {
            "text": "Submit",
            "color": {
                "red": 0,
                "blue": 0,
                "green": 0
            },
            "onClick": {
                "action": {
                    "function": "https://helloworld-s2377xozpq-uc.a.run.app/track-item",
                    "parameters": [
                        {
                            "key": "selectedFiles",
                            "value": json.dumps(selected_files)
                        }
                    ],
                    "persistValues": False
                }
            }
        },
        "secondaryButton": {
            "text": "Cancel",
            "color": {
                "red": 0,
                "blue": 0,
                "green": 0
            },
            "onClick": {
                "openLink": {
                    "url": "www.dropbox.com",
                    "onClose": "NOTHING",  # Change this
                    "openAs": "OVERLAY"
                }
            }
        }
    }
    card.update_action()
    card.create_card("Files selected", fixed_footer)
    card.add_section("Enter emails to be notified", False)
    auxMethods.add_widgets(selected_files, card)
    card.add_widget("textInput", text_input)
    button_list = {
        "buttons": [
            auxMethods.build_add_email_button(card.get_card(), text_input)  # Might want to do this as having a
        ]                                                                   # counter to count the number add email buttons,
    }                                                                       # and then create that number of buttons
    card.add_widget("buttonList", button_list)
    return card


def contextual_card(selected_items):
    card_title = "Selected Items" if (len(selected_items) > 1) else selected_items[0]["title"]
    fixed_footer = {
        "primaryButton": {
            "text": "Download File",
            "color": {
                "red": 0,
                "blue": 0,
                "green": 0
            },
            "onClick": {
                "openDynamicLinkAction": {
                    "function": "https://helloworld-s2377xozpq-uc.a.run.app/download-file-bytes"
                }
            }
        },
        "secondaryButton": {
            "text": "Cancel",  # Set this up so that a previous card would appear
            "color": {
                "red": 0.32421,
                "blue": 0.23421,
                "green": 0.2353614
            },
            "onClick": {
                "openLink": {
                    "url": "www.google.com",  # Change this later
                    "onClose": "NOTHING",
                    "openAs": "FULL_SIZE"
                }
            }
        }
    }
    image_item = {
        "imageUrl": selected_items[0]["iconUrl"]
    }
    card = Card(card_title)
    card.update_action()
    card.create_card("Selected File", fixed_footer)
    card.add_section("Selected File", False)
    card.add_widget("image", image_item)
    return json.dumps(card.display_card())


def notification_card(text):
    submit_form_response = {
        "renderActions": {
            "action": {
                "notification": {
                    "text": text
                }
            }
        }
    }
    return json.dumps(submit_form_response)

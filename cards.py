import json
from Backend import apiMethods as Methods
import auxillaryMethods as auxMethods
from card import Card
import uuid


# Return the json representation of the homepage.
#
# Args:
#   page_token: the page token for the page of files or folders.
#
# Returns:
#   The json representation of the homepage card
def homepage_card(page_token=0):
    folder_card = list_card(False, page_token)
    file_card = list_card(True, page_token)

    # This will direct users who click on it to the list of folders
    decorated_text_folders = {
        "topLabel": "Select Folders",
        "text": "Select folders to track",
        "onClick": {
            "card": folder_card.get_card()
        }
    }

    # This will direct users who click on it to the list of files
    decorated_text_files = {
        "topLabel": "Select Files",
        "text": "Select Files to track",
        "onClick": {
            "card": file_card.get_card()
        }
    }

    # Create the card
    home_card = Card("Main Card")
    home_card.create_card("Files or Folders to track")
    home_card.update_action()
    home_card.add_section("Go to Folders or Files", False)
    home_card.add_widget("decoratedText", decorated_text_folders)
    home_card.add_widget("decoratedText", decorated_text_files)
    return home_card.display_card()


# Get the json representation of the list of folders or the list of files.
#
# Args:
#   file_flag: a bool that determines if the card is being created for
#   files or for folders.
#   page_token: the page token for the page of files or folders to be
#   used in the list.
#
# Returns:
#   The json representation of the list card.
def list_card(file_flag, page_token):
    item_list_card = Card(f"{'Files' if file_flag else 'Folders'} Card")
    if file_flag:
        response = Methods.file_list_response("mimeType!='application/vnd.google-apps.folder'", page_token)
    else:
        response = Methods.file_list_response("mimeType='application/vnd.google-apps.folder'", page_token)

    next_page_token = response["nextPageToken"] if "nextPageToken" in response else -1
    tuple_of_folders_and_files = auxMethods.filter_items(response["files"])
    items = tuple_of_folders_and_files[file_flag]  # the items will either folders or files depending on the flag

    # This fixed_footer contains the buttons that allows users to submit the selected files to the item tracking card
    # and [another button].
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
            "text": "Does nothing",  # Change this button to do something
            "color": {
                "red": 0,
                "blue": 0,
                "green": 0
            },
            "disabled": True,
            "onClick": {
                "openLink": {
                    "url": "www.google.com",
                    "onClose": "NOTHING",
                    "openAs": "OVERLAY"
                }
            }
        }
    }
    # These buttons are the buttons user can use to go back and forth
    # in the pages of the file and folder results.
    buttons = {
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
    # This widget contains the list of results indicated by the page_token along with
    # a checkbox next to each item.
    selection_input_item = {
        "name": "Selection Input",
        "label": "Selection Input",
        "type": "CHECK_BOX",
        "items": json.loads(auxMethods.create_list_items(items)),
    }

    # Create the card
    item_list_card.update_action()
    item_list_card.create_card(f"{'Files' if file_flag else 'Folders'} to Watch", fixed_footer)
    item_list_card.add_section(f"Select {'Files' if file_flag else 'Folders'}", False)
    item_list_card.add_widget("selectionInput", selection_input_item)
    item_list_card.add_widget("buttonList", buttons)
    return item_list_card


# Get the json representation of the item tracking card.
#
# Args:
#   selected_files: The json representation of the files selected.
#
# Returns:
#   The Card object containing the json representation of the
#   item tracking card.
def item_tracking_card(selected_files):
    card = Card("Notifications")
    email_attribute_name = str(uuid.uuid4())
    # This text input contains the field where users can enter their emails
    text_input = {
        "name": f"Email {email_attribute_name}",
        "label": "Enter Email",
        "value": "",
    }
    # This fixed_footer contains the buttons that allows users to submit the
    # provided emails to be associated with the selected files
    # and [implement the cancel button].
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
    # Create the card
    card.update_action()
    card.create_card("Files selected", fixed_footer)
    card.add_section("Enter emails to be notified", False)
    auxMethods.add_text_widgets(selected_files, card)
    card.add_widget("textInput", text_input)
    # Create the "add email" button. This must be done after
    # creating the card so that the entire json representation of the
    # card used in the parameters field of the request sent to /track-item
    # can be created.
    button_list = {
        "buttons": [
            auxMethods.build_add_email_button(card.get_card(), text_input)  # Might want to do this as having a
        ]                                                                   # counter to count the number add email buttons,
    }                                                                       # and then create that number of buttons
    card.add_widget("buttonList", button_list)
    return card


# Return the json representation of the notification card.
#
# Args:
#   text: The text used in the notification.
#
# Returns:
#   The json representation of the notification card.
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

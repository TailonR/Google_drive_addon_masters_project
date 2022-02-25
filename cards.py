import json
from Backend import apiMethods as Methods
import auxillaryMethods as auxMethods
from Backend import datastoreMethods as Datastore
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

    fixed_footer = {
        "primaryButton": {
            "text": "Stop Tracking",
            "color": {
                "red": 0,
                "blue": 0,
                "green": 0
            },
            "disabled": False if len(Datastore.get_all_file_ids_tracked()) > 0 else True,
            "onClick": {
                "action": {
                    "function": "https://helloworld-s2377xozpq-uc.a.run.app/stop-tracking",
                }
            }
        }
    }

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
    home_card.create_card("Files or Folders to track", fixed_footer)
    home_card.update_action()
    home_card.add_section("Go to Folders or Files", False)
    home_card.add_widget("decoratedText", decorated_text_folders)
    home_card.add_widget("decoratedText", decorated_text_files)
    return home_card.display_card()


# Get the Card representing a card containing either the list of folders or of files.
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

    # This fixed_footer contains the buttons that allows users to submit the selected files to the item tracking card.
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
        "items": auxMethods.create_list_items_for_list_card(response["files"]),
    }
    decorated_text = {
        "text": "<b>Note: Tracking a folder results in tracking of any files within the folder</b>",
        "wrapText": True
    }

    # Create the card
    item_list_card.update_action()
    item_list_card.create_card(f"{'Files' if file_flag else 'Folders'} to Watch", fixed_footer)
    item_list_card.add_section(f"Select {'Files' if file_flag else f'Folders'}", False)
    item_list_card.add_widget("decoratedText", decorated_text)
    item_list_card.add_widget("selectionInput", selection_input_item)
    item_list_card.add_widget("buttonList", buttons, "CENTER")
    return item_list_card


# Get the Card representing the item tracking card.
# The item tracking card contains the names of the files selected,
# fields to enter emails, and buttons to track or to not track those files.
#
# Args:
#   selected_files: The json representation of the files selected.
#
# Returns:
#   The Card object containing the json representation of the
#   item tracking card.
def item_tracking_card(selected_files, previous_email_inputs=None):
    card = Card("Notifications")
    # This fixed_footer contains the buttons that allows users to submit the provided emails to be associated
    # with the selected files and that allows users to end tracking of the selected files.
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
            "text": "Stop Tracking",
            "color": {
                "red": 0,
                "blue": 0,
                "green": 0
            },
            "onClick": {
                "action": {
                    "function": "https://helloworld-s2377xozpq-uc.a.run.app/end-tracking",
                    "parameters": [
                        {
                            "key": "selectedFiles",
                            "value": json.dumps(selected_files)
                        }
                    ],
                }
            }
        }
    }
    decorated_text = {
        "text": "<b>Note: Tracking a folder results in tracking of any files within the folder</b>",
        "wrapText": True
    }
    text_paragraph = {
        "text": "Selected Files:"
    }

    # Create the card
    card.update_action()
    card.create_card("Files selected", fixed_footer)
    card.add_section("Enter emails to be notified", False)
    card.add_widget("decoratedText", decorated_text)
    card.add_widget("textParagraph", text_paragraph)
    # Display the file names on the card
    auxMethods.add_text_widgets(selected_files, card)

    # If a user clicked the "add email" button then we need to add
    # the text inputs that contain the emails the user already entered
    # to the new card.
    if previous_email_inputs is not None:
        for email_input in previous_email_inputs:
            card.add_widget("textInput", email_input["textInput"])

    # The text input contains the field where users can enter their emails.
    # The value of this field (not to be confused with the value attribute of text_input)
    # is passed to the add_email function request so that previously entered emails
    # can be preserved in the new card.
    email_attribute_name = str(uuid.uuid4())
    text_input = {
        "name": f"Email {email_attribute_name}",
        "label": "Enter Email",
        "value": "",
    }
    card.add_widget("textInput", text_input)

    # This button list contains the button to add an email.
    # The url that the button calls is given by the function attribute of
    # the onClick action.
    # The request to this url will pass parameters to it, as indicated
    # by the parameters attribute of the onClick action.
    # In order to make a new card it needs to be the same as the old card,
    # just with an additional textInput.
    # Therefore the parameters given are the previously entered emails, and
    # the selected items.
    button_list = {
        "buttons": [
            {
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
                                "key": "previousEmailInputs",
                                "value": json.dumps(card.get_widgets("textInput"))
                            },
                            {
                                "key": "selectedFiles",
                                "value": json.dumps(selected_files)
                            }
                        ],
                        "persistValues": True
                    }
                }
            }
        ]
    }
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
    return submit_form_response


# Get the json representation of the list of folders and files being tracked.
#
# Returns:
#   The json representation of the list card.
def stop_tracking_card(tracked_files_info):
    # This fixed_footer contains a submit button which, once clicked,
    # sends the selected files to the end_tracking function
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
                    "function": "https://helloworld-s2377xozpq-uc.a.run.app/end-tracking",
                }
            }
        }
    }

    # This widget contains the list of results indicated by the page_token along with
    # a checkbox next to each item.
    selection_input_item = {
        "name": "Selection Input",
        "label": "Selection Input",
        "type": "CHECK_BOX",
        "items": auxMethods.create_list_items_for_stop_tracking_card(tracked_files_info),
    }

    # Create the card
    card = Card("Stop Tracking Card")
    card.update_action()
    card.create_card(" Files/Folders to Stop Watching", fixed_footer)
    card.add_section("Select Files/Folders", False)
    card.add_widget("selectionInput", selection_input_item)
    return card

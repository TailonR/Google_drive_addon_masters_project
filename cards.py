import json
from Backend import apiMethods as Methods
import auxillaryMethods as auxMethods
from Backend import authorization
from card import Card
import uuid


def homepage_card(page_token=0):
    url = authorization.get_authorization_url()

    link_action = {
        "openDynamicLinkAction": {
            "function": "https://dummy-function-from-resources.net/openLinkCallback"
        }
    }
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
                    "function": "https://helloworld-s2377xozpq-uc.a.run.app/file-to-be-tracked",
                }
            }
        },
        "secondaryButton": {
            "text": "Authorize Test",
            "color": {
                "red": 0,
                "blue": 0,
                "green": 0
            },
            "onClick": {
                "openLink": {
                    "url": url,
                    "onClose": "NOTHING",  # Change this
                    "openAs": "OVERLAY"
                }
            }
        }
    }

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
    home_card.create_card_action("Unknown use of card action", link_action)
    return home_card.display_card()


# This function takes a folder flag which is a bool that determines if we are creating
# a card for a list of folders or a list of files.
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
                    "function": "https://helloworld-s2377xozpq-uc.a.run.app/file-to-be-tracked",
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


def item_to_be_tracked_card(selected_files):
    card = Card("Notifications")
    email_attribute_name = str(uuid.uuid4())
    text_input = {
        "name": f"Email {email_attribute_name}",
        "label": "Enter Email",
        "value": "",
    }
    # Possible attributes
    #     "onChangeAction":,
    #     "initialSuggestions":,
    #     "autoCompleteAction":,
    #     "multipleSuggestions":,
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


# Creates a card with two widgets.
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

# def homepage_card():
#     card = {
#         "action": {
#             "navigations": [
#                 {
#                     "pushCard": {
#                         "header": {
#                             "title": "Main Card"
#                         },
#                         "name": "Main Card",
#                         "peekCardHeader": {
#                             "title": "This is a peek card",
#                             "imageType": "SQUARE",
#                             "imageUrl": "http://ssl.gstatic.com/travel-trips-fe/icon_hotel_grey_64.png",
#                             "imageAltText": "Image of Cards",
#                             "subtitle": "No Subtitle"
#                         },
#                         "cardActions": [
#                             {
#                                 "actionLabel": "This is Card action - 1",
#                                 "onClick": {
#                                     "openDynamicLinkAction": {
#                                         "function": "https://dummy-function-from-resources.net/openLinkCallback"
#                                     }
#                                 }
#                             },
#                             {
#                                 "actionLabel": "This is Card action - 2",
#                                 "onClick": {
#                                     "action": {
#                                         "function": "https://dummy-function-from-resources.net/generic_submit_form_response"
#                                     }
#                                 }
#                             },
#                             {
#                                 "actionLabel": "This is Card action - 3",
#                                 "onClick": {
#                                     "openLink": {
#                                         "onClose": "RELOAD",
#                                         "openAs": "OVERLAY",
#                                         "url": "https://dummy-function-from-resources.net/open_link_sample"
#                                     }
#                                 }
#                             },
#                             {
#                                 "actionLabel": "This is Card action - 4",
#                                 "onClick": {
#                                     "card": {
#                                         "header": {
#                                             "title": "This card is shown after card action 4 is clicked"
#                                         },
#                                         "sections": [
#                                             {
#                                                 "widgets": [
#                                                     {
#                                                         "textParagraph": {
#                                                             "text": "This is a sample text for the card that's shown after action 4 of the card is clicked"
#                                                         }
#                                                     }
#                                                 ]
#                                             }
#                                         ]
#                                     }
#                                 }
#                             }
#                         ],
#                         "fixedFooter": {
#                             "primaryButton": {
#                                 "text": "Primary Button",
#                                 "color": {
#                                     "red": 0,
#                                     "blue": 0,
#                                     "green": 0
#                                 },
#                                 "onClick": {
#                                     "openLink": {
#                                         "url": "www.google.ca",
#                                         "onClose": "NOTHING",
#                                         "openAs": "FULL_SIZE"
#                                     }
#                                 }
#                             },
#                             "secondaryButton": {
#                                 "text": "Secondary Button - Disabled",
#                                 "disabled": True,
#                                 "color": {
#                                     "red": 0.32421,
#                                     "blue": 0.23421,
#                                     "green": 0.2353614
#                                 },
#                                 "onClick": {
#                                     "openLink": {
#                                         "url": "www.google.com",
#                                         "onClose": "NOTHING",
#                                         "openAs": "FULL_SIZE"
#                                     }
#                                 }
#                             }
#                         },
#                         "sections": [
#                             {
#                                 "header": "Section 1 - Date Time",
#                                 "collapsible": True,
#                                 "widgets": [
#                                     {
#                                         "dateTimePicker": {
#                                             "name": "Date Time Picker - EST",
#                                             "label": "Date Time Picker - EST",
#                                             "valueMsEpoch": 1585166673000,
#                                             "onChangeAction": {
#                                                 "function": "https://dummy-function-from-resources.net/sample_notification"
#                                             },
#                                             "timezoneOffsetDate": -240,
#                                             "type": "DATE_AND_TIME"
#                                         }
#                                     },
#                                     {
#                                         "dateTimePicker": {
#                                             "name": "Date Picker - CST",
#                                             "label": "Date Time Picker - CST",
#                                             "valueMsEpoch": 1585166673000,
#                                             "onChangeAction": {
#                                                 "function": "https://dummy-function-from-resources.net/sample_notification"
#                                             },
#                                             "timezoneOffsetDate": -300,
#                                             "type": "DATE_AND_TIME"
#                                         }
#                                     },
#                                     {
#                                         "dateTimePicker": {
#                                             "name": "Date Time Picker - PST",
#                                             "label": "Date Time Picker - PST",
#                                             "valueMsEpoch": 1585166673000,
#                                             "onChangeAction": {
#                                                 "function": "https://dummy-function-from-resources.net/sample_notification"
#                                             },
#                                             "timezoneOffsetDate": -420,
#                                             "type": "DATE_AND_TIME"
#                                         }
#                                     }
#                                 ]
#                             },
#                             {
#                                 "header": "Section 2 - Decorated Text",
#                                 "collapsible": True,
#                                 "uncollapsibleWidgetsCount": 2,
#                                 "widgets": [
#                                     {
#                                         "decoratedText": {
#                                             "topLabel": "Top Label - Decorated Text CHECKBOX",
#                                             "switchControl": {
#                                                 "controlType": "CHECKBOX",
#                                                 "name": "Name - Check Box Sample",
#                                                 "value": "Value - Check Box Sample"
#                                             },
#                                             "text": "Text - Decorated Text",
#                                             "bottomLabel": "Bottom Label - Decorated Text CHECKBOX",
#                                             "wrapText": False,
#                                             "onClick": {
#                                                 "card": {
#                                                     "header": {
#                                                         "title": "Decorated Text - On Click Action Card"
#                                                     },
#                                                     "sections": [
#                                                         {
#                                                             "widgets": [
#                                                                 {
#                                                                     "image": {
#                                                                         "imageUrl": "https://cataas.com/cat/says/hello%20world!",
#                                                                         "altText": "Hello World - Cat Image"
#                                                                     }
#                                                                 }
#                                                             ]
#                                                         }
#                                                     ]
#                                                 }
#                                             }
#                                         }
#                                     },
#                                     {
#                                         "decoratedText": {
#                                             "topLabel": "Top Label - Decorated Text SWITCH",
#                                             "switchControl": {
#                                                 "controlType": "SWITCH",
#                                                 "name": "Name - SWITCH Sample",
#                                                 "value": "Value - SWITCH Sample"
#                                             },
#                                             "text": "Text - Decorated Text",
#                                             "bottomLabel": "Bottom Label - Decorated Text SWITCH",
#                                             "wrapText": False,
#                                             "onClick": {
#                                                 "card": {
#                                                     "header": {
#                                                         "title": "Decorated Text - On Click Action Card"
#                                                     },
#                                                     "sections": [
#                                                         {
#                                                             "widgets": [
#                                                                 {
#                                                                     "image": {
#                                                                         "imageUrl": "https://cataas.com/cat/says/hello%20world!",
#                                                                         "altText": "Hello World - Cat Image",
#                                                                         "onClick": {
#                                                                             "action": {
#                                                                                 "function": "https://dummy-function-from-resources.net/pop_to_root"
#                                                                             }
#                                                                         }
#                                                                     }
#                                                                 }
#                                                             ]
#                                                         }
#                                                     ]
#                                                 }
#                                             }
#                                         }
#                                     },
#                                     {
#                                         "decoratedText": {
#                                             "topLabel": "Top Label - Decorated Text Button",
#                                             "bottomLabel": "Bottom Label - Decorated Text Button",
#                                             "text": "Text - Decorated Text Button",
#                                             "button": {
#                                                 "icon": {
#                                                     "altText": "Assessment Blue",
#                                                     "icon_url": "http://ssl.gstatic.com/travel-trips-fe/icon_hotel_grey_64.png"
#                                                 },
#                                                 "text": "Assessment Blue",
#                                                 "onClick": {
#                                                     "openLink": {
#                                                         "url": "http://ssl.gstatic.com/travel-trips-fe/icon_hotel_grey_64.png",
#                                                         "openAs": "OVERLAY",
#                                                         "onClose": "RELOAD"
#                                                     }
#                                                 }
#                                             }
#                                         }
#                                     },
#                                     {
#                                         "decoratedText": {
#                                             "topLabel": "Top Label - Decorated Text CHECKBOX",
#                                             "switchControl": {
#                                                 "controlType": "CHECKBOX",
#                                                 "name": "Name - Check Box Sample",
#                                                 "value": "Value - Check Box Sample"
#                                             },
#                                             "text": "Text - Decorated Text",
#                                             "bottomLabel": "Bottom Label - Decorated Text CHECKBOX",
#                                             "wrapText": False,
#                                             "onClick": {
#                                                 "card": {
#                                                     "header": {
#                                                         "title": "Decorated Text - On Click Action Card"
#                                                     },
#                                                     "sections": [
#                                                         {
#                                                             "widgets": [
#                                                                 {
#                                                                     "image": {
#                                                                         "imageUrl": "https://cataas.com/cat/says/hello%20world!",
#                                                                         "altText": "Hello World - Cat Image"
#                                                                     }
#                                                                 }
#                                                             ]
#                                                         }
#                                                     ]
#                                                 }
#                                             }
#                                         }
#                                     },
#                                     {
#                                         "decoratedText": {
#                                             "topLabel": "Top Label - Decorated Text Icon",
#                                             "bottomLabel": "Bottom Label - Decorated Text Icon",
#                                             "text": "Text - Decorated Text Icon",
#                                             "icon": {
#                                                 "iconUrl": "http://ssl.gstatic.com/travel-trips-fe/icon_hotel_grey_64.png",
#                                                 "altText": "Arrow Right Blue"
#                                             }
#                                         }
#                                     },
#                                     {
#                                         "decoratedText": {
#                                             "topLabel": "Top Label - Decorated Text Wrap",
#                                             "bottomLabel": "Bottom Label - Decorated Text Wrap",
#                                             "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam fringilla facilisis ne.",
#                                             "wrapText": True
#                                         }
#                                     },
#                                     {
#                                         "decoratedText": {
#                                             "topLabel": "Top Label - Decorated Text Non-Wrap",
#                                             "bottomLabel": "Bottom Label - Decorated Text Non-Wrap",
#                                             "text": "Nunc ultrices massa ut nisl porttitor, ut euismod nisl tincidunt. Vivamus pharetra, est sed sagittis consequat, arcu nisi.",
#                                             "wrapText": False
#                                         }
#                                     }
#                                 ]
#                             },
#                             {
#                                 "header": "Section 3 - Button List",
#                                 "collapsible": True,
#                                 "widgets": [
#                                     {
#                                         "buttonList": {
#                                             "buttons": [
#                                                 {
#                                                     "icon": {
#                                                         "iconUrl": "http://ssl.gstatic.com/travel-trips-fe/icon_hotel_grey_64.png",
#                                                         "altText": "G - Button"
#                                                     },
#                                                     "color": {
#                                                         "red": 0,
#                                                         "blue": 0,
#                                                         "green": 1
#                                                     },
#                                                     "disabled": False,
#                                                     "onClick": {
#                                                         "openLink": {
#                                                             "url": "www.google.ca/"
#                                                         }
#                                                     },
#                                                     "text": "Green - Google.ca"
#                                                 },
#                                                 {
#                                                     "color": {
#                                                         "red": 1,
#                                                         "blue": 0,
#                                                         "green": 0
#                                                     },
#                                                     "disabled": False,
#                                                     "onClick": {
#                                                         "action": {
#                                                             "function": "https://dummy-function-from-resources.net/pop_to_card_2"
#                                                         }
#                                                     },
#                                                     "text": "Pop to Card 2"
#                                                 },
#                                                 {
#                                                     "color": {
#                                                         "red": 0,
#                                                         "blue": 1,
#                                                         "green": 0
#                                                     },
#                                                     "disabled": False,
#                                                     "onClick": {
#                                                         "openLink": {
#                                                             "url": "www.google.ca/"
#                                                         }
#                                                     },
#                                                     "text": "Blue - Google"
#                                                 },
#                                                 {
#                                                     "color": {
#                                                         "red": 1,
#                                                         "blue": 1,
#                                                         "green": 1
#                                                     },
#                                                     "disabled": True,
#                                                     "onClick": {
#                                                         "openLink": {
#                                                             "url": "www.google.ca/"
#                                                         }
#
#                                                     },
#                                                     "text": "Disabled Button"
#                                                 }
#                                             ]
#                                         }
#                                     }
#                                 ]
#                             },
#                             {
#                                 "header": "Section 4 - Images",
#                                 "collapsible": True,
#                                 "widgets": [
#                                     {
#                                         "image": {
#                                             "imageUrl": "http://ssl.gstatic.com/travel-trips-fe/icon_hotel_grey_64.png",
#                                             "onClick": {
#                                                 "openLink": {
#                                                     "url": "http://ssl.gstatic.com/travel-trips-fe/icon_hotel_grey_64.png",
#                                                     "openAs": "FULL_SIZE",
#                                                     "onClose": "NOTHING"
#                                                 }
#                                             }
#                                         }
#                                     },
#                                     {
#                                         "image": {
#                                             "imageUrl": "http://ssl.gstatic.com/travel-trips-fe/icon_hotel_grey_64.png",
#                                             "altText": "Commute - Black",
#                                             "onClick": {
#                                                 "openLink": {
#                                                     "url": "http://ssl.gstatic.com/travel-trips-fe/icon_hotel_grey_64.png",
#                                                     "openAs": "FULL_SIZE",
#                                                     "onClose": "RELOAD"
#                                                 }
#                                             }
#                                         }
#                                     }
#                                 ]
#                             },
#                             {
#                                 "header": "Section 5 - Text Paragraph",
#                                 "collapsible": True,
#                                 "widgets": [
#                                     {
#                                         "textParagraph": {
#                                             "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam fringilla facilisis neque, condimentum egestas dolor dapibus id."
#                                         }
#                                     }
#                                 ]
#                             },
#                             {
#                                 "header": "Section 6 - Selection Input",
#                                 "collapsible": True,
#                                 "widgets": [
#                                     {
#                                         "selectionInput": {
#                                             "name": "Selection Input Check box",
#                                             "label": "Selection Input Check box",
#                                             "type": "CHECK_BOX",
#                                             "items": [
#                                                 {
#                                                     "text": "Selection Input item 1 Text",
#                                                     "value": "Selection Input item 1 Value"
#                                                 },
#                                                 {
#                                                     "text": "Selection Input item 2 Text",
#                                                     "value": "Selection Input item 2 Value"
#                                                 }
#                                             ],
#                                             "onChangeAction": {
#                                                 "function": "https://us-central1-driveaddon-2122.cloudfunctions.net/testing_when_box_is_checked"
#                                             }
#                                         }
#                                     },
#                                     {
#                                         "selectionInput": {
#                                             "name": "Selection Input Dropdown",
#                                             "label": "Selection Input Dropdown",
#                                             "type": "DROPDOWN",
#                                             "items": [
#                                                 {
#                                                     "text": "Selection Input item 1 Text",
#                                                     "value": "Selection Input item 1 Value"
#                                                 },
#                                                 {
#                                                     "text": "Selection Input item 2 Text",
#                                                     "value": "Selection Input item 2 Value"
#                                                 }
#                                             ]
#                                         }
#                                     },
#                                     {
#                                         "selectionInput": {
#                                             "name": "Selection Input Radio",
#                                             "label": "Selection Input Radio",
#                                             "type": "RADIO_BUTTON",
#                                             "items": [
#                                                 {
#                                                     "text": "Selection Input item 1 Text",
#                                                     "value": "Selection Input item 1 Value"
#                                                 },
#                                                 {
#                                                     "text": "Selection Input item 2 Text",
#                                                     "value": "Selection Input item 2 Value"
#                                                 }
#                                             ]
#                                         }
#                                     },
#                                     {
#                                         "selectionInput": {
#                                             "name": "Selection Input Switch",
#                                             "label": "Selection Input Switch",
#                                             "type": "SWITCH",
#                                             "items": [
#                                                 {
#                                                     "text": "Selection Input item 1 Text",
#                                                     "value": "Selection Input item 1 Value"
#                                                 },
#                                                 {
#                                                     "text": "Selection Input item 2 Text",
#                                                     "value": "Selection Input item 2 Value"
#                                                 }
#                                             ]
#                                         }
#                                     }
#                                 ]
#                             }
#                         ]
#                     }
#                 }
#             ]
#         }
#     }
#     return json.dumps(card)

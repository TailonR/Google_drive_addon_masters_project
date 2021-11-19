import json
from google.cloud import logging
from google.cloud import datastore
import Backend.apiMethods as apiMethods
import Backend.datastoreMethods as dataMethods
import Backend.authorization as authorization
import Backend.channel as channel

html = '''
<html>
    <head>
        <title> Testing </title>
        <meta name="google-site-verification" content="8psgssS-xesgoyjpqsuMaQF8hylryMb_gBbF2FzWJn8"/>
    </head>
<body>
'''


#
#  Google Cloud Function that loads the homepage for a
#  Google Workspace Add-on.
#
#  @param {Object} req Request sent from Google
#
def load_homepage(req):
    return create_action()


# # Creates a card with two widgets.
# def create_action():
#     card = {
#         "$schema": "/Users/dummy_user/Documents/JSON_schema/renderActionSchema.json",
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


# Creates a card with two widgets.
def create_action():
    url = authorization.get_authorization_url()
    card = {
        "action": {
            "navigations": [
                {
                    "pushCard": {
                        "header": {
                            "title": "Main Card"
                        },
                        "name": "Files to watch",
                        "cardActions": [
                            {
                                "actionLabel": "Unknown use of card action",
                                "onClick": {
                                    "openDynamicLinkAction": {
                                        "function": "https://dummy-function-from-resources.net/openLinkCallback"
                                    }
                                }
                            }
                        ],
                        "fixedFooter": {
                            "primaryButton": {
                                "text": "Primary Button",
                                "color": {
                                    "red": 0,
                                    "blue": 0,
                                    "green": 0
                                },
                                "onClick": {
                                    "openLink": {
                                        "url": url,
                                        "onClose": "NOTHING",
                                        "openAs": "OVERLAY"
                                    }
                                }
                            }
                        },
                        "sections": [
                            {
                                "header": "Select files",
                                "collapsible": False,
                                "widgets": [
                                    {
                                        "selectionInput": {
                                            "name": "Selection Input Switch",
                                            "label": "Selection Input Switch",
                                            "type": "SWITCH",
                                            "items": json.loads(json.dumps(create_list_items())),
                                            "onChangeAction": {
                                                "function": "https://us-central1-driveaddon-2122.cloudfunctions.net/testing_when_box_is_checked",
                                                "persistValues": True
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }
    return json.dumps(card)


def test_new_card(name):
    submit_form_response = {
        "renderActions": {
            "action": {
                "notification": {
                    "text": f"{name} has been added"
                }
            }
        }
    }
    return json.dumps(submit_form_response)


# To use logging:
#   logger = logging.Client().logger("logger_name")
#   logger.log_text(whatever_variable_or_text)
# def respond_to_trigger(req):
#     creds = authenticate()
#     service = create_service('gmail', 'v1', creds)
#     user_info = service.users().getProfile(userId='me').execute()
#     the_sender = user_info["emailAddress"]
#     the_recipient = "tailrusse2020@gmail.com"
#     the_subject = "testing again again and again"
#     the_text = "You should see this when I select a file"
#     the_message = create_message(the_sender, the_recipient, the_subject, the_text)
#     send_message(service, "me", the_message)
#     request_json = req.get_json(silent=True)
#     selected_itmes = request_json["drive"]["selectedItems"]
#     first_item = selected_itmes[0]
#     return create_card(first_item["title"], first_item["iconUrl"])


def trigger(req):
    cred = authorization.authenticate()
    logger = logging.Client().logger("logger_name")
    changes = get_recent_changes()
    logger.log_text(f"The changes: {changes}")
    return create_action()


def get_recent_changes():
    cred = authorization.authenticate()
    drive_service = apiMethods.create_service("drive", "v3", cred)
    client = datastore.Client("driveaddon-2122", credentials=cred)
    current_page_token = dataMethods.get_current_page_token(client)
    changes = drive_service.changes().list(pageToken=current_page_token["startPageToken"]).execute()
    page_token = drive_service.changes().getStartPageToken().execute()
    # store_new_start_page_token(client, page_token)
    print(json.dumps(changes, indent=4))
    print(page_token)
    return changes


def get_files(page_token=0):
    cred = authorization.authenticate()
    drive_service = apiMethods.create_service("drive", "v3", cred)
    client = datastore.Client("driveaddon-2122", credentials=cred)
    if page_token == 0:
        response = drive_service.files().list().execute()
    else:
        response = drive_service.files().list(pageToken=page_token).execute()

    return response['files']


def create_list_items(page_token=0):
    files = []
    files.extend(get_files(page_token))
    files_list = []
    for file in files:
        file_to_add = {
            "text": file['name'],
            "value": f"Selection Input {file['name']} Value"
        }
        files_list.append(file_to_add)
    return files_list


def get_string_input_values(form_submit_response):
    return form_submit_response["commonEventObject"]["formInputs"]["Selection Input Switch"]["stringInputs"]["value"]


def get_item_name(input_value):
    input_value = input_value.replace("Selection Input", "")
    input_value = input_value.replace("Value", "")
    input_value = input_value.strip()
    return input_value


def testing_when_box_is_checked(req):
    req_json = req.get_json(silent=True)
    input_values = get_string_input_values(req_json)
    item_name = get_item_name(input_values[0])
    file_id = ""
    files = get_files()
    for file in files:
        if file['name'] == item_name:
            file_id = file['id']
    channel.dev_create_channel(file_id)
    return test_new_card(item_name)


channel.dev_stop_channel()
# channel.dev_create_channel()
# get_recent_changes()
# trigger(1)
# create_list_items()
# testing_when_box_is_checked(1)

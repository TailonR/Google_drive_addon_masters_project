import json
from google.cloud import logging
from google.cloud import datastore
import Backend.apiMethods as apiMethods
import Backend.datastoreMethods as dataMethods
import Backend.authorization as authorization

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


# Creates a card with two widgets.
def create_action():
    card = {
        "action": {
            "navigations": [
                {
                    "pushCard": {
                        "header": {
                            "title": "Cats!"
                        },
                        "sections": [
                            {
                                "widgets": [
                                    {
                                        "textParagraph": {
                                            "text": "Your random cat:"
                                        }
                                    },
                                    {
                                        "image": {
                                            "imageUrl": "https://aiptcomics.com/wp-content/uploads/2019/09/JUL190885.jpg"
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


def create_widgets():
    widgets = {
        "widgets": [
            {
                "textParagraph": {
                    "text": ""
                }
            },
            {
                "image": {
                    "imageUrl": "https://cataas.com/cat"
                }
            }
        ]
    }
    return widgets


def create_sections():
    sections = create_widgets()
    return sections


def create_push_card():
    push_card = {
        "header": {
            "title": "rgarsgaragw"
        },
        "sections": create_sections()
    }
    return push_card


def create_card(title, icon_url):
    card = {
        "action": {
            "navigations": [
                {
                    "pushCard": {
                        "header": {
                            "title": title
                        },
                        "sections": [
                            {
                                "widgets": [
                                    {
                                        "textParagraph": {
                                            "text": "The icon is:"
                                        }
                                    },
                                    {
                                        "image": {
                                            "imageUrl": icon_url
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


def respond_to_trigger(req):
    url = authorization.dev_authenticate()
    card = {
        "action": {
            "navigations": [
                {
                    "pushCard": {
                        "header": {
                            "title": "What the hell"
                        },
                        "sections": [
                            {
                                "widgets": [
                                    {
                                        "buttonList": {
                                            "buttons": [
                                                {
                                                    "icon": {
                                                        "iconUrl": "http://ssl.gstatic.com/travel-trips-fe/icon_hotel_grey_64.png",
                                                        "altText": "G - Button"
                                                    },
                                                    "color": {
                                                        "red": 0,
                                                        "blue": 0,
                                                        "green": 1
                                                    },
                                                    "disabled": False,
                                                    "onClick": {
                                                        "openLink": {
                                                            "url": url
                                                        }
                                                    },
                                                    "text": "Green - Google.ca"
                                                }
                                            ]
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
    # page_token = drive_service.changes().getStartPageToken().execute()
    # store_new_start_page_token(client, page_token)
    current_page_token = dataMethods.get_current_page_token(client)
    print(current_page_token["startPageToken"])
    changes = drive_service.changes().list(pageToken=current_page_token["startPageToken"]).execute()
    return changes


# dev_stop_channel()
# dev_create_channel()
# get_recent_changes()
# trigger(1)


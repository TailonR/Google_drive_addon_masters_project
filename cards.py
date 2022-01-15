import json
from Backend import apiMethods as Methods
from Backend import authorization


def homepage_card():
    url = authorization.get_authorization_url()
    card = {
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
                        "onClose": "NOTHING",  # Change this
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
                            "items": json.loads(json.dumps(Methods.create_list_items())),
                            "onChangeAction": {
                                "function": "https://helloworld-s2377xozpq-uc.a.run.app/create-channel",  # Change this
                                "persistValues": True
                            }
                        }
                    }
                ]
            }
        ]
    }
    render_action = {
        "action": {
            "navigations": [
                {
                    "pushCard": card
                }
            ]
        }
    }
    return json.dumps(render_action)


# Creates a card with two widgets.
def item_selected_card(selected_items):
    card_title = "Selected Items" if (len(selected_items) > 1) else selected_items[0]["title"]

    card = {
        "header": {
            "title": card_title
        },
        "name": "Files to watch",
        "fixedFooter": {
            "primaryButton": {
                "text": "Download File",
                "color": {
                    "red": 0,
                    "blue": 0,
                    "green": 0
                },
                "onClick": {
                    "openDynamicLinkAction": {
                        "function": "www.google.com" # Consider changing this
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
        },
        "sections": [
            {
                "header": "Files to download",
                "collapsible": False,
                "widgets": [
                    {
                        "image": {
                            "imageUrl": selected_items[0]["iconUrl"]
                        }
                    }  # Add the widgets here
                ]
            }
        ]
    }

    render_action = {
        "action": {
            "navigations": [
                {
                    "pushCard": card
                }
            ]
        }
    }
    return json.dumps(render_action)


def notification_card(name):
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
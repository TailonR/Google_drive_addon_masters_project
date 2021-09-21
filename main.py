import json

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
    cards = {
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
                                            "imageUrl": "https://cataas.com/cat"
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
    return json.dumps(cards)

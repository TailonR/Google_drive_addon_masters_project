class Card:
    def __init__(self, data):
        if isinstance(data, str):
            self._widgets = []
            self._sections = []
            self._card_actions = []
            self._card_header = {}
            self._action = {}
            self._card = {}
            self._header = {
                "title": data
            }
        elif isinstance(data, dict):
            self.create_card_from_json(data)

    def create_card_from_json(self, card_json):
        self._widgets = card_json["sections"][0]["widgets"]
        self._sections = card_json["sections"]
        self._card_actions = card_json["cardActions"]
        self._card_header = card_json["peekCardHeader"]
        self._card = card_json
        self._header = {
            "title": card_json["header"]["title"]
        }
        self.update_action()

    def add_section(self, header, collapsible, uncollapsible_widgets_count=0):
        self._sections.append({
            "header": header,
            "collapsible": collapsible,
            "uncollapsibleWidgetsCount": uncollapsible_widgets_count,
            "widgets": self._widgets
        })

    def add_widget(self, widget_item_type, widget_item, horizontal_alignment="START"):
        self._widgets.append({
            "horizontalAlignment": horizontal_alignment,
            widget_item_type: widget_item
        })

    def create_card_header(self, title, subtitle, image_type, image_url, image_alt_text):
        self._card_header = {
            "title": title,
            "subtitle": subtitle,
            "imageType": image_type,
            "imageUrl": image_url,
            "imageAltText": image_alt_text
        }

    def update_card_header(self, card_header):
        self._card["peakCardHeader"] = card_header

    def create_card(self, name_id, card_fixed_footer=None, display_style="REPLACE"):
        self._card = {
            "header": self._header,
            "sections": self._sections,
            "cardActions": self._card_actions,
            "name": name_id,
            "fixedFooter": card_fixed_footer,
            "displayStyle": display_style,
            "peekCardHeader": self._card_header
        }
        self.update_action()

    def get_button_list(self):
        return self._card["sections"]["widgets"]["buttonList"]

    def insert_card(self):
        self._action = {
            "action": {
                "navigations": [
                    {
                        "pushCard": self._card
                    }
                ]
            }
        }

    def create_card_action(self, label, on_click_action):
        self._card_actions.append({
            "actionLabel": label,
            "onClick": on_click_action
        })

    def update_action(self):
        self._action = {
            "action": {
                "navigations": [
                    {
                        "pushCard": self._card
                    }
                ]
            }
        }

    def replace_card(self):
        return {
            "renderActions": {
                "action": {
                    "navigations": [
                        {
                            "pop": True
                        },
                        {
                            "pushCard": self._card
                        }
                    ]
                }
            }
        }

    def push_card(self):
        return {
            "renderActions": self._action  # used to be get_action()
        }

    def display_card(self):
        return self._action

    def get_card(self):
        return self._card

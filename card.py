# Class Card.
#
# This class create a json representation
# of a card.
# This class contains methods that will return
# json objects that instructs Google Workspace
# on how to add the card to the stack.
class Card:
    def __init__(self, data):
        self._widgets = []
        self._sections = []
        self._card_actions = []
        self._card_header = {}
        self._action = {}
        self._card = {}
        self._header = {
            "title": data
        }

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

    # Return the json representation of the card.
    # The navigations tell Google Workspace that
    # it should remove the previous card and to
    # push this card to the stack.
    #
    # Returns:
    #   A json representation of the card and actions
    #   that Google Workspace should conduct.
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

    # Return the widgets of the card.
    # The parameter "kind" indicates the kind of widgets
    # to return.
    # If no kind is provided then return all the widgets.
    #
    # Returns:
    #   The widgets of the card.
    def get_widgets(self, kind=None):
        if kind is not None:
            specific_widgets = []
            for widget in self._widgets:
                if kind in widget:
                    specific_widgets.append(widget)
            return specific_widgets
        else:
            return self._widgets

    # Return the json representation of the card.
    # This function tells Google Workspace to push
    # the card as a render instruction.
    #
    # Returns:
    #   A json representation of the card with render
    #   instructions.
    def push_card(self):
        return {
            "renderActions": self._action  # used to be get_action()
        }

    # Return json representation of the card.
    # This simply tells Google Workspace to
    # push the card to the stack.
    #
    # Returns:
    #   A json representation of the card and actions
    #   that Google Workspace should conduct.
    def display_card(self):
        return self._action

    # Return json representation of the card.
    # This simply returns the card with no instructions
    #
    # Returns:
    #   A json representation of the card.
    def get_card(self):
        return self._card

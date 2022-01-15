def get_item_name(input_value):
    input_value = input_value.replace("Selection Input", "")
    input_value = input_value.replace("Value", "")
    input_value = input_value.strip()
    return input_value


def get_string_input_values(form_submit_response):
    return form_submit_response["commonEventObject"]["formInputs"]["Selection Input Switch"]["stringInputs"]["value"]

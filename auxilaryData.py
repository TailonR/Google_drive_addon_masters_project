import Backend.authorization as authorization
import Backend.apiMethods as apiMethods

# could add multiple options for types that have multiple compatible types
export_data = {"application/vnd.google-apps.document": 6,
               "application/vnd.google-apps.drawing": 1,
               "application/vnd.google-apps.presentation": 2,
               "application/vnd.google-apps.spreadsheet": 3}


def get_destination_format(destination_data, mime_type):
    mime_type_index = destination_data[mime_type]
    return get_export_formats()[mime_type][mime_type_index]  # Could add multiple options for downloading a certain format


# Think about making cred and drive_service a class so that you don't have to create cred and drive_service all the time
def get_export_formats():
    cred = authorization.authenticate()
    drive_service = apiMethods.create_service("drive", "v3", cred)
    response = drive_service.about().get(fields="exportFormats").execute()
    return response["exportFormats"]
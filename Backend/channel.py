import json
from google.cloud import logging
from googleapiclient import errors
import uuid
from Backend.apiMethods import create_service
import Backend.datastoreMethods as datastoreMethods


#############################################
# Delete this once the project is finished
#############################################
def dev_create_channel(file_id):
    drive_service, cred = create_service("drive", "v3")
    logger = logging.Client().logger("logger_name")

    body = {
        'id': "324475b8-afb2-48c7-913e-0d853ea71ff9",
        'token': cred.token,
        'type': "web_hook",
        'address': "https://helloworld-s2377xozpq-uc.a.run.app/trigger"
    }

    try:
        response = drive_service.files().watch(fileId=file_id, body=body).execute()
        logger.log_text(json.dumps(response, indent=4))
    except errors.HttpError as error:
        raise error


#############################################
# Delete this once the project is finished
#############################################
def dev_create_channel_changes():
    drive_service, cred = create_service("drive", "v3")
    logger = logging.Client().logger("logger_name")

    body = {
        'id': "324475b8-afb2-48c7-913e-0d853ea71ff9",
        'token': cred.token,
        'type': "web_hook",
        'address': "https://helloworld-s2377xozpq-uc.a.run.app/new-file-added"
    }

    try:
        current_page_token = drive_service.changes().getStartPageToken().execute()
        response = drive_service.changes().watch(body=body, pageToken=current_page_token).execute()
        logger.log_text(json.dumps(response, indent=4))
    except errors.HttpError as error:
        raise error


#############################################
# Delete this once the project is finished
#############################################
def dev_stop_channel(channel_id, resource_id):
    drive_service, _ = create_service("drive", "v3")

    body = {
        'id': channel_id,
        'resourceId': resource_id
    }

    try:
        drive_service.channels().stop(body=body).execute()
    except errors.HttpError as error:
        print("An error occurred:", error)


def create_channel(file_id):
    drive_service, cred = create_service("drive", "v3")
    logger = logging.Client().logger("logger_name")

    channel_id = str(uuid.uuid4())
    body = {
        'id': channel_id,
        'token': cred.token,
        'type': "web_hook",
        'address': "https://helloworld-s2377xozpq-uc.a.run.app/trigger"
    }

    try:
        response = drive_service.files().watch(fileId=file_id, body=body).execute()
        datastoreMethods.store_channel_info(channel_id, response["resourceId"], file_id)
        logger.log_text(json.dumps(response, indent=4))
    except errors.HttpError as error:
        raise error


def create_channel_changes():
    drive_service, cred = create_service("drive", "v3")
    logger = logging.Client().logger("logger_name")

    channel_id = str(uuid.uuid4())
    body = {
        'id': channel_id,
        'token': cred.token,
        'type': "web_hook",
        'address': "https://helloworld-s2377xozpq-uc.a.run.app/new-file-added"
    }

    try:
        current_page_token = drive_service.changes().getStartPageToken().execute()
        response = drive_service.changes().watch(body=body, pageToken=current_page_token["startPageToken"]).execute()
        datastoreMethods.store_channel_info(channel_id, response["resourceId"])
        logger.log_text(json.dumps(response, indent=4))
    except errors.HttpError as error:
        raise error


def stop_channel(file_id="changes"):
    drive_service, _ = create_service("drive", "v3")
    channel_info = datastoreMethods.get_channel_info(file_id)
    channel_id = channel_info["channelId"]
    resource_id = channel_info["resourceId"]

    body = {
        'id': channel_id,
        'resourceId': resource_id
    }

    try:
        drive_service.channels().stop(body=body).execute()
        datastoreMethods.delete_channel_entity(file_id)
    except errors.HttpError as error:
        print("An error occurred:", error)


import json
from google.cloud import logging
from googleapiclient import errors
import uuid
from Backend.apiMethods import create_service
import Backend.datastoreMethods as datastoreMethods


def create_channel():
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
        current_page_token = drive_service.changes().getStartPageToken().execute()
        response = drive_service.changes().watch(body=body, pageToken=current_page_token["startPageToken"]).execute()
        datastoreMethods.store_channel_info(channel_id, response["resourceId"])
        logger.log_text(json.dumps(response, indent=4))
    except errors.HttpError as error:
        raise error


def stop_channel():
    drive_service, _ = create_service("drive", "v3")
    channel_info = datastoreMethods.get_channel_info()
    channel_id = channel_info["channelId"]
    resource_id = channel_info["resourceId"]

    body = {
        'id': channel_id,
        'resourceId': resource_id
    }

    try:
        drive_service.channels().stop(body=body).execute()
        datastoreMethods.delete_datastore_entity("Channels", "changes")
    except errors.HttpError as error:
        print("An error occurred:", error)

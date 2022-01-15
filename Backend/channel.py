import json
from google.cloud import logging
from googleapiclient import errors
import uuid
from Backend.apiMethods import create_service


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
        print("An error occurred:", error)


def dev_stop_channel():
    drive_service, _ = create_service("drive", "v3")

    # body = {
    #     'id': "324475b8-afb2-48c7-913e-0d853ea71ff9",
    #     'resourceId': "HOuCEMqvWIxw8YjvZfr4tDKYor8"
    # }

    # body = {
    #     'id': "324475b8-afb2-48c7-913e-0d853ea71ff9",
    #     'resourceId': "dSWGJjFHcnLREW5WgnHT9IQL-eU"
    # }

    # body = {
    #     'id': "324475b8-afb2-48c7-913e-0d853ea71ff9",
    #     'resourceId': "WZWFx3Y_f1R0EwzeflupSc_e2eQ"
    # }

    body = {
        'id': "324475b8-afb2-48c7-913e-0d853ea71ff9",
        'resourceId': "onBImpQLM_bAiNHDRPz3CajVGPs"
    }

    try:
        drive_service.channels().stop(body=body).execute()
    except errors.HttpError as error:
        print("An error occurred:", error)


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
        page_token = drive_service.changes().getStartPageToken().execute()
        response = drive_service.changes().watch(pageToken=page_token['startPageToken'], body=body).execute()
        logger.log_text(json.dumps(response, indent=4))
    except errors.HttpError as error:
        print("An error occurred:", error)


def stop_channel(channel_id, resource_id):
    drive_service, _ = create_service("drive", "v3")

    body = {
        'id': channel_id,
        'resourceId': resource_id
    }

    try:
        drive_service.channels().stop(body=body).execute()
    except errors.HttpError as error:
        print("An error occurred:", error)

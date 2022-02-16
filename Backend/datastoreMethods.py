import json
from datetime import datetime
from google.cloud import datastore


def store_token(client: datastore.Client, creds):
    key = client.key("Tokens")
    token_entity = datastore.Entity(key)
    json_creds = creds.to_json()
    loaded_creds = json.loads(json_creds)
    token_entity.update({
        "created": datetime.now(),
        "token": loaded_creds["token"],
        "refresh_token": loaded_creds["refresh_token"],
        "token_uri": loaded_creds["token_uri"],
        "client_id": loaded_creds["client_id"],
        "client_secret": loaded_creds["client_secret"],
        "scopes": loaded_creds["scopes"],
        "expiry": loaded_creds["expiry"]
    })
    client.put(token_entity)


def get_most_recent_token(client: datastore.Client):
    query = client.query(kind="Tokens")
    query.order = ["created"]
    results = list(query.fetch())
    if len(results) > 0:
        return results[len(results) - 1]
    else:
        return None


def token_exists():
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="Tokens")
    query.order = ["created"]
    results = list(query.fetch())
    if len(results) > 0:
        return True
    else:
        return False


def store_emails(file_ids, emails):
    datastore_client = datastore.Client()
    for file_id in file_ids:
        if get_emails(file_id) is not None:
            continue
        complete_key = datastore_client.key("Emails", file_id)
        email_entity = datastore.Entity(key=complete_key)
        email_entity.update({
            "start": datetime.now(),
            "emails": emails
        })
        datastore_client.put(email_entity)


def get_emails(file_id):
    datastore_client = datastore.Client()
    key = datastore_client.key("Emails", file_id)
    results = datastore_client.get(key)
    if results is not None:
        return results["emails"]
    else:
        return None


def store_channel_info(channel_id, resource_id):
    datastore_client = datastore.Client()
    key = datastore_client.key("Channels", "changes")
    channel_entity = datastore.Entity(key=key)
    channel_entity.update({
        "channelId": channel_id,
        "resourceId": resource_id
    })
    datastore_client.put(channel_entity)


def get_channel_info():
    datastore_client = datastore.Client()
    key = datastore_client.key("Channels", "changes")
    results = datastore_client.get(key)
    return results


def delete_datastore_entity(kind, file_id):
    datastore_client = datastore.Client()
    key = datastore_client.key(kind, file_id)
    datastore_client.delete(key)

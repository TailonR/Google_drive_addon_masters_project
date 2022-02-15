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


def store_new_start_page_token(client: datastore.Client, start_page_token):
    key = client.key("StartPageTokens")
    page_token_entity = datastore.Entity(key)
    page_token_entity.update({
        "kind": start_page_token["kind"],
        "startPageToken": start_page_token["startPageToken"]
    })
    client.put(page_token_entity)


def get_current_page_token(client: datastore.Client):
    query = client.query(kind="StartPageTokens")
    query.order = ["startPageTokens"]
    results = list(query.fetch())
    if len(results) > 0:
        return results[len(results) - 1]
    else:
        return None


def get_most_recent_token(client: datastore.Client):
    query = client.query(kind="Tokens")
    query.order = ["created"]
    results = list(query.fetch())
    if len(results) > 0:
        return results[len(results) - 1]
    else:
        return None


def store_emails(file_ids, emails):
    datastore_client = datastore.Client()
    # The kind for the new entity
    kind = "Emails"

    for file_id in file_ids:
        # file_id will be name/ID for the new entity
        complete_key = datastore_client.key(kind, file_id)

        email_entity = datastore.Entity(key=complete_key)

        email_entity.update({
            "start": datetime.now(),
            "emails": emails
        })

        datastore_client.put(email_entity)


def get_emails(file_id):
    client = datastore.Client()
    kind = "Emails"
    query = client.query(kind=kind)
    first_key = client.key(kind, file_id)
    # key_filter(key, op) translates to add_filter('__key__', op, key).
    query.key_filter(first_key, "=")
    results = list(query.fetch())[0]
    return results["emails"]


def store_channel_info(channel_id, resource_id, file_id="changes"):
    datastore_client = datastore.Client()
    # The kind for the new entity
    kind = "Channels"

    # file_id will be name/ID for the new entity
    key = datastore_client.key("Channels", file_id)

    channel_entity = datastore.Entity(key=key)

    channel_entity.update({
        "channelId": channel_id,
        "resourceId": resource_id
    })

    datastore_client.put(channel_entity)


def get_channel_info(file_id="changes"):
    datastore_client = datastore.Client()
    key = datastore_client.key("Channels", file_id)
    results = datastore_client.get(key)
    return results


def delete_channel_entity(file_id):
    datastore_client = datastore.Client()
    kind = "Channels"
    key = datastore_client.key(kind, file_id)
    datastore_client.delete(key)

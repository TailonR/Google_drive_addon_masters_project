import json
from datetime import datetime
from google.cloud import datastore


def store_token(client: datastore.Client, creds):
    key = client.key("Token")
    token = datastore.Entity(key)
    json_creds = creds.to_json()
    loaded_creds = json.loads(json_creds)
    token.update({
        "created": datetime.now(),
        "token": loaded_creds["token"],
        "refresh_token": loaded_creds["refresh_token"],
        "token_uri": loaded_creds["token_uri"],
        "client_id": loaded_creds["client_id"],
        "client_secret": loaded_creds["client_secret"],
        "scopes": loaded_creds["scopes"],
        "expiry": loaded_creds["expiry"]
    })
    client.put(token)


def store_new_start_page_token(client: datastore.Client, start_page_token):
    key = client.key("StartPageToken")
    page_token = datastore.Entity(key)
    page_token.update({
        "kind": start_page_token["kind"],
        "startPageToken": start_page_token["startPageToken"]
    })
    client.put(page_token)


def get_current_page_token(client: datastore.Client):
    query = client.query(kind="StartPageToken")
    query.order = ["startPageToken"]
    results = list(query.fetch())
    if len(results) > 0:
        return results[len(results) - 1]
    else:
        return None


def get_most_recent_token(client: datastore.Client):
    query = client.query(kind="Token")
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

        task = datastore.Entity(key=complete_key)

        task.update(
            {
                "start": datetime.now(),
                "emails": emails
            }
        )

        datastore_client.put(task)


def get_emails(file_id):
    client = datastore.Client()
    kind = "Emails"
    query = client.query(kind=kind)
    first_key = client.key(kind, file_id)
    # key_filter(key, op) translates to add_filter('__key__', op, key).
    query.key_filter(first_key, "=")
    results = list(query.fetch())[0]
    return results["emails"]


def get_tracking_info():
    datastore_client = datastore.Client()
    query = datastore_client.query()
    query.keys_only()

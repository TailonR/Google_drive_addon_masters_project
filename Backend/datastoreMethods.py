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
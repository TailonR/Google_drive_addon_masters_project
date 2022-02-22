import json
import time
from google.cloud import datastore
from datetime import datetime

# Store a new token.
#
# Args:
#   client: a client used for interacting with
#   the datastore.
#   creds: The creds used to authenticate the addon
#   and which will be stored in the datastore.
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


# Get the most recently created token.
#
# Args:
#   client: a client used for interacting with
#   the datastore.
#
# Returns:
#   The most recent token or none if no token exists.
def get_most_recent_token(client: datastore.Client):
    query = client.query(kind="Tokens")
    query.order = ["created"]
    results = list(query.fetch())
    if len(results) > 0:
        return results[len(results) - 1]
    else:
        return None


# Determines if any token exists.
#
# Returns:
#   True if there exists a token, False otherwise.
def token_exists():
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="Tokens")
    query.order = ["created"]
    results = list(query.fetch())
    if len(results) > 0:
        return True
    else:
        return False


# Store the file information of file to be tracked.
#
# Args:
#   file_ids: the ids that will be stored in the datastore.
#   emails: the emails associated with the file_ids.
#   parent_id: the parent of the file.
def store_file_info(file_id, file_name, emails):
    datastore_client = datastore.Client()
    complete_key = datastore_client.key("TrackedFiles", file_id)
    email_entity = datastore.Entity(key=complete_key)
    email_entity.update({
        "fileName": file_name,
        "emails": emails,
    })
    datastore_client.put(email_entity)


# Get the file information associated with the given file_id.
# Such information includes the parent_id and the email addresses to
# Args:
#   file_id: the id to look for in the datastore.
#   attribute: the attribute to return.
#
# Returns:
#   The table entities associated with given the file_id in their key
#   or none if it doesn't exist.
#   If no file_id is provided, all entries in the table
#   If no attribute, all entity attributes
def get_tracked_file_info(file_id=None, attribute=None):
    datastore_client = datastore.Client()
    if file_id is not None and attribute is not None:  # Return the given attribute of the given file_id
        key = datastore_client.key("TrackedFiles", file_id)
        result = datastore_client.get(key)
        if result is not None:
            return result[attribute]
        else:
            return None
    elif file_id is not None and attribute is None:  # Return the entire entity of the given file_id
        key = datastore_client.key("TrackedFiles", file_id)
        result = datastore_client.get(key)
        if result is not None:
            return result
        else:
            return None
    elif file_id is None and attribute is None:  # Return all entities in the table
        query = datastore_client.query(kind="TrackedFiles")
        return list(query.fetch())


# Store the channel information.
#
# Args:
#   channel_id: the channel_id for the channel.
#   resource_id: the resource_id for the channel.
def store_channel_info(channel_id, resource_id, expiration):
    datastore_client = datastore.Client()
    key = datastore_client.key("Channels", "changes")
    channel_entity = datastore.Entity(key=key)
    channel_entity.update({
        "channelId": channel_id,
        "resourceId": resource_id,
        "expiration": expiration
    })
    datastore_client.put(channel_entity)


# Get channel information.
#
# Returns:
#   The channel information.
def get_channel_info():
    datastore_client = datastore.Client()
    key = datastore_client.key("Channels", "changes")
    results = datastore_client.get(key)
    return results


# Delete a datastore entity.
#
# Args:
#   kind: the kind of the entity to be deleted.
#   file_id: the file_id of the entity to be deleted.
def delete_datastore_entity(kind, file_id):
    datastore_client = datastore.Client()
    key = datastore_client.key(kind, file_id)
    datastore_client.delete(key)


# Delete multiple datastore entities of the same kind.
#
# Args:
#   kind: the kind of the entity to be deleted.
#   file_ids: the file_ids of the entities to be deleted.
def delete_datastore_entities(kind, file_ids):
    datastore_client = datastore.Client()
    keys = []
    for file_id in file_ids:
        keys.append(datastore_client.key(kind, file_id))

    datastore_client.delete_multi(keys)

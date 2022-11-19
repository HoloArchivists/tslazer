import json

import requests


def get_user_id(screen_name):
    """Convert Twitter Screen Name to ID

    Args:
        screen_name (str): Twitter User Screen Name

    Returns:
        str: Twitter User ID
    """
    # Get the User ID of a single twitter user
    url = "https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names=" + screen_name
    user_req = requests.get(url, timeout=10)
    user_json = json.loads(user_req.text)
    return user_json[0]["id"]

def get_screen_name(user_id):
    """Convert Twitter User ID to Screen Name

    Args:
        user_id (str): Twitter User ID

    Returns:
        str: screen name
    """
    # Get the screen name of a single twitter user
    url = "https://cdn.syndication.twimg.com/widgets/followbutton/info.json?user_ids=" + user_id
    user_req = requests.get(url, timeout=10)
    user_json = json.loads(user_req.text)
    return user_json[0]["screen_name"]

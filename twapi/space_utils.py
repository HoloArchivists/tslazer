import json

import requests

# Requires Cookies and Auth Token

def check_user(user_id, auth_token, cookies):
    """Check if User ID is hosting a twitter space

    Args:
        user_id (str): _description_
        auth_token (str): _description_
        cookies (str): _description_

    Returns:
        space_id (str) or None: Return None if no Space, Return space ID otherwise
    """
    # Check a single ID for a space
    # If the user is hosting a space, return the ID, otherwise return None
    check_url = "https://twitter.com/i/api/fleets/v1/avatar_content?user_ids=" + user_id
    headers = {"Authorization": auth_token,
               "cookie": cookies}
    space_req = requests.get(check_url, headers=headers, timeout=5)
    space_req_json = json.loads(space_req.text)
    if space_req_json["refresh_delay_secs"] != 0:
        return space_req_json["users"][user_id]["spaces"]["live_content"]["audiospace"]["broadcast_id"]
    else:
        return None

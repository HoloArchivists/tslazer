import json
import logging
import time
from urllib.parse import quote

import requests

# Guest API Adaptation for get_space.py
# GET Request
URL = "https://twitter.com/i/api/graphql/Ha9BKBF0uAz9d4-lz0jnYA/AudioSpaceById"

features = {"spaces_2022_h2_clipping":False,
            "spaces_2022_h2_spaces_communities":True,
            "responsive_web_twitter_blue_verified_badge_is_enabled":True,
            "verified_phone_label_enabled":False,
            "tweetypie_unmention_optimization_enabled":True,
            "responsive_web_uc_gql_enabled":True,
            "vibe_api_enabled":True,
            "responsive_web_edit_tweet_api_enabled":False,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled":True,
            "standardized_nudges_misinfo":True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":False,
            "responsive_web_graphql_timeline_navigation_enabled":True,
            "interactive_text_enabled":True,
            "responsive_web_text_conversations_enabled":False,
            "responsive_web_enhance_cards_enabled":True}

# Extratable Meta:
# rest_id, state, title, media_key, created at (unix), started_at (unix), updated_at (unix),
# creator Rest ID, creator created at, creator description,
# profile image url https, screen name, url, participants etc
def get_space_guest(space_id, guest_token):
    """Use the Twitter Guest API to get Twitter Space Information

    Args:
        space_id (str): Space ID
        guest_token (str): Twitter Guest Token

    Returns:
        _type_: json
    """
    variables = {"id": space_id,
                "isMetatagsQuery":True,
                "withSuperFollowsUserFields":True,
                "withDownvotePerspective":False,
                "withReactionsMetadata":False,
                "withReactionsPerspective":False,
                "withSuperFollowsTweetFields":True,
                "withReplays":True}
    headers = {"authorization" : "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA", 
               "x-guest-token" : guest_token}
    space_info = requests.get(URL + f"?variables={quote(json.dumps(variables))}&features={quote(json.dumps(features))}", timeout=10, headers=headers)
    space_info_json = json.loads(space_info.text)
    return space_info_json

# Use Get Media Key from get_space.py

def wait_for_end_guest(space_id, metadata, guest_token, interval=30):
    """Wait for a Twitter Space to End, being careful not to burn the guest token

    Args:
        space_id (str): Twitter Space ID
        metadata (json): Twitter Space Metadata
        guest_token (str): guest token
        interval (int, optional): heartbeat interval to check the space status. Defaults to 30.
    """
    # Check Periodically to see if the space is over. Return a value when it does.
    if metadata["data"]["audioSpace"]["metadata"]["state"] == "Running":
        print("[TSLAZER] Valid Space Detected. Waiting for Space to end...")
        print(f"[TSLAZER] Querying the Space at an interval of {interval} seconds")
        running = True
        while running is True:
            is_running = get_space_guest(space_id, guest_token)
            if is_running["data"]["audioSpace"]["metadata"]["state"] == "Running":
                running = True
            else:
                running = False
            time.sleep(interval)
    else:
        pass

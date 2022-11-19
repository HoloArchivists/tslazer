import requests
import json

# GET Request, only needs Guest Key and Guest Token
URL = "https://twitter.com/i/api/1.1/live_video_stream/status/" # + media key

def get_data_guest(media_key, guest_token):
    """Get Space URLs From Guest Token

    Args:
        media_key (string): the media key for the twitter space
        guest_token (string): twitter guest API token

    Returns:
        _type_: json
    """
    headers = {"authorization" : "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                "x-guest-token" : guest_token}
    url_query = requests.get(URL + media_key, headers=headers, timeout=10)
    url_data = json.loads(url_query.text)
    return url_data # Return the raw info, then make another function to parse it,
    # to help keep everything seperate

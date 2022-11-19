import json
import requests

# GET Request, only needs auth and cookies
URL = "https://twitter.com/i/api/1.1/live_video_stream/status/" # + media key

def get_data(media_key, authtoken, cookies):
    """Get The Twitter Space URLs from the media key

    Args:
        media_key (str): Media Key
        authtoken (str): Auth Token
        cookies (str): cookies

    Returns:
        _type_: _description_
    """
    headers = {"cookie": cookies,
               "Authorization": authtoken}
    url_query = requests.get(URL + media_key, headers=headers, timeout=10)
    url_data = json.loads(url_query.text)
    return url_data # Return the raw info, then make another function to parse it,
    # to help keep everything seperate

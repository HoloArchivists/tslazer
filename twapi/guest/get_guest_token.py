import requests

def get_guest_token():
    """
    Generate a guest token for use with the Twitter API. Note: Twitter will get mad if you call this too many times

    :returns: string
    """
    headers = {"authorization" : "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"}
    token_request = requests.post("https://api.twitter.com/1.1/guest/activate.json", timeout=10, headers=headers)
    token_response = token_request.json()
    return token_response["guest_token"]

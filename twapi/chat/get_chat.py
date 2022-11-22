import requests
import json
import twapi.parsing.chat_parser as chat_parser

# The chat downloading module is not completed yet

def get_chat_access_tokens(chat_token):
    url = "https://proxsee.pscp.tv/api/v2/accessChatPublic"
    payload = {"chat_token": chat_token}

    token_request = requests.post(url, data=json.dumps(payload))
    token_response = token_request.json()

    return (token_response["replay_endpoint"] + '/chatapi/v1/history', token_response["replay_access_token"], token_response["auth_token"], token_response["access_token"], token_response["endpoint"], token_response["participant_index"], token_response["room_id"])

def chat_request(chat_replay_endpoint, chat_replay_token, cursor=""):
    """Retrieve the chat messages

    Args:
        chat_replay_endpoint (str): _description_
        chat_replay_token (str): chat replay token
        cursor (str, optional): Cursor. Defaults to "".

    Returns:
        _type_: _description_
    """
    url = chat_replay_endpoint
    payload = {"access_token" : chat_replay_token, "cursor": cursor, "limit":100}
    chat_request = requests.post(url, data=json.dumps(payload), timeout=10)
    
    if chat_request.status_code == 503:
        # Twitter Space Over, No more Chat
        return (None, None)
    chat_response = json.loads(chat_request.text)
    return(chat_response["messages"], chat_response["cursor"])
    
def get_chat_messages(chat_replay_endpoint, chat_replay_token):
    chat_messages = []
    list_concat = lambda l: any(map(chat_messages.append, l))
    chat_log, cursor = chat_request(chat_replay_endpoint, chat_replay_token, cursor="")
    list_concat(chat_log)
    while chat_log and cursor is not None:
        chat_log, cursor = chat_request(chat_replay_endpoint, chat_replay_token, cursor=cursor)
        print(f"[TSLAZER] ChatEngine: Collected {len(chat_messages)} Messages", end="\r")
        list_concat(chat_log)
    return chat_messages

def parse_all_messages(messages):
    msg = list()
    for message in messages:
        msg.append(chat_parser.parse_message(message))
    return msg
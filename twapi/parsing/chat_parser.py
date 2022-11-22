import json
# These are sent as "types" in body of the payload
# I've seen 1, 45, and 2. These are the only codes transmitted in the message logs.
# I'm unsure how to get the other ones, though.
# This is the payload "type" tag. if any. From what I see, there cannot exist a type and kind
# tag in the same payload message.
recordable_action_types = {
        0 : "Unknown",
        1 : "Chat",
        2 : "Reaction", # User sent a reaction, I know this much (Original was "Heart")
        3 : "Join",
        4 : "Location",
        5 : "BroadcastEnded",
        6 : "InviteFollowers",
        7 : "BroadcastStartedLocally",
        8 : "BroadcasterUploadedReplay",
        9 : "Timestamp",
        10 : "LocalPromptToFollowBroadcaster",
        11 : "LocalPromptToShareBroadcast",
        12 : "BroadcasterBlockedViewer",
        13 : "SubscriberSharedOnTwitter",
        14 : "SubscriberBlockedViewer",
        15 : "SubscriberSharedOnFacebook",
        16 : "Screenshot",
        29 : "Sentence",
        36 : "Sparkle",
        37 : "FirstSparkle",
        39 : "CommentMuted",
        40 : "HydraControlMessage",
        41 : "CommentMutedByModerator",
        42 : "CommentUnmutedByModerator",
        43 : "LocalShouldReportGuestUser",
        44 : "UserIsTyping",
        45 : "ServerAudioTranscription",
        201 : "ChatCaption"
}

sendable_action_types = {
1 : "Join",
2 : "Leave", # User Left the space
3 : "Roster",
4 : "Presence", # Query the amount of listeners in the space
8 : "Ban"
}

user_action_types = {
1 : "Chat", # Usual Code to represent Chat in the message logs
2 : "Control", # User Joined/Left (Control Of The Roster)
3 : "Auth" # This is used to get the access token for the chat (When Joining via websocket)
}

# How this whole thing works
# Take the first "kind" variable from the message, look that up in the user action types
# If the user action type is control, then look the second kind in the sendable action types
# If the user action type is chat, then check the type variable in the recordable action types

def parse_message(msg):
        # For each kind of message we want to provide a readable message in the chat logs
        parsed_message = {}
        message_kind = user_action_types[msg["kind"]]
        message_payload = json.loads(msg["payload"])
        parsed_message['MessageType'] = message_kind
        if message_kind == 'Control':
                parsed_message['Action'] = sendable_action_types[message_payload['kind']]
                parsed_message['MessageSender'] = {}
                parsed_message['MessageSender']['user_id'] =  message_payload.get("sender", {}).get("user_id")
                parsed_message['MessageSender']['username'] = message_payload.get("sender", {}).get("username")
                parsed_message['MessageSender']['display_name'] = message_payload.get("sender", {}).get("display_name")
                parsed_message['MessageSender']['profile_image_url'] = message_payload.get("sender", {}).get("profile_image_url")
                parsed_message['MessageSender']['locale'] = message_payload.get("sender", {}).get("locale")
                parsed_message['MessageSender']['twitter_id'] = message_payload.get("sender", {}).get("twitter_id")
                parsed_message['MessageSender']['lang'] = message_payload.get("sender", {}).get("lang")
                parsed_message['Signature'] = msg['signature']
        if message_kind == 'Chat':
                parsed_message['Action'] = user_action_types[msg['kind']]
                if message_payload.get('body'):
                        message_body = json.loads(message_payload.get("body"))
                        parsed_message['ActionType'] = recordable_action_types[message_body.get("type")]
                        parsed_message['Body'] = message_body.get("body")
                        parsed_message["Emoji"] = message_body.get("emoji")
                        parsed_message["GuestParticipantIndex"] = message_body.get("guestParticipantIndex")
                        parsed_message["Participant_Index"] = message_body.get("participant_index")
                        parsed_message["GuestUsername"] = message_body.get("guestUsername")
                        parsed_message["ProgramDateTime"] = message_body.get("programDateTime")
                parsed_message['Timestamp'] = message_payload.get("timestamp")
                parsed_message['MessageSender'] = {}
                if message_payload.get("sender"):
                        parsed_message['MessageSender']['user_id'] =  message_payload.get("sender", {}).get("user_id")
                        parsed_message['MessageSender']['username'] = message_payload.get("sender", {}).get("username")
                        parsed_message['MessageSender']['display_name'] = message_payload.get("sender", {}).get("display_name")
                        parsed_message['MessageSender']['profile_image_url'] = message_payload.get("sender", {}).get("profile_image_url")
                        parsed_message['MessageSender']['locale'] = message_payload.get("sender", {}).get("locale")
                        parsed_message['MessageSender']['twitter_id'] = message_payload.get("sender", {}).get("twitter_id")
                        parsed_message['MessageSender']['lang'] = message_payload.get("sender", {}).get("lang")
                if message_payload.get("uuid"):
                        parsed_message['UUID'] = message_payload["uuid"]
                parsed_message['Signature'] = msg['signature']
                
        return parsed_message
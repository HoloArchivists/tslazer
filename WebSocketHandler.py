# WebSocketHandler.py
# Written By ef1500
# Purpose: Export Twitter Space Chats
import os
import json
import requests
import collections

from dataclasses import dataclass

class SpaceChat:
    TwitterUser = collections.namedtuple('TwitterUser', ['name', 'screen_name', 'id'])
    Bearer = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
    
    @dataclass
    class ChatVars:
        chat_replay_endpoint: str # Replay Var
        chat_replay_token: str    # Replay Var
        auth_token: str           # Live Var
        access_token: str         # Live Var
        endpoint: str             # Live Var
        participant_index: str    # Live Var
        room_id: str

    @dataclass
    class ChatData:
        messages: list
        cursor: int
        
    @dataclass
    class PayloadSender:
        sender_user_id: str
        sender_username: str
        sender_display_name: str
        sender_profile_url: str
        
    @dataclass
    class PayloadSenderLite:
        sender_user_id: str
        

    # I've barely got any clue what these maps mean, they show up in https://abs.twimg.com/responsive-web/client-web/shared~loader.AudioDock~bundle.AudioSpaceAnalytics~bundle.AudioSpacePeek~bundle.AudioSpaceReport~bundle.Birdw.71332e28.js
    # And when you recieve the JSON, it seems apparent that it uses Type 1 for the Chat Logs when they're sent,
    # and then it prefers the Ad

    # These are actions that are sent to the server (I Think)
    UserActions = {
        1 : "Chat", # Usual Code to represent Chat in the message logs
        2 : "Control", # User Joined/Left (Control Of The Roster)
        3 : "Auth" # This is used to get the access token for the chat (When Joining via websocket)
    }

    # Sendable actions, I think
    # This is the inner "kind" tag, if any.
    SendableActions = {
        1 : "Join",
        2 : "Leave", # User Left the space
        3 : "Roster",
        4 : "Presence", # Query the amount of listeners in the space
        8 : "Ban"
    }

    # These are sent as "types" in body of the payload
    # I've seen 1, 45, and 2. These are the only codes transmitted in the message logs.
    # I'm unsure how to get the other ones, though.
    # This is the payload "type" tag. if any. From what I see, there cannot exist a type and kind
    # tag in the same payload message.
    RecordableActionTypes = {
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

    # To start, let's get the tokens, we're gonna need that
    @staticmethod
    def get_tokens(chat_token):
        url = "https://proxsee.pscp.tv/api/v2/accessChatPublic"
        payload = {"chat_token": chat_token}

        tokenRequest = requests.post(url, data=json.dumps(payload))
        tokenResponse = tokenRequest.json()

        return SpaceChat.ChatVars(tokenResponse["replay_endpoint"] + '/chatapi/v1/history', tokenResponse["replay_access_token"], tokenResponse["auth_token"], tokenResponse["access_token"], tokenResponse["endpoint"], tokenResponse["participant_index"], tokenResponse["room_id"])

    # This is likely to be better for getting the chat history after the twitter space has already ended.
    # I will make a seperate function to create the websocket that retrtieves the message history live.
    # It might be more beneficial to use these in conjunction, that way once we have all of the history,
    # We can start getting the live chat history.
    @staticmethod
    def get_chatData(chatvars, cursor=""):
        url = f"{chatvars.chat_replay_endpoint}"
        payload = {"access_token" : chatvars.chat_replay_token,"cursor" : cursor, "limit":100}

        chatrequest = requests.post(url, data=json.dumps(payload))
        if chatrequest.status_code == 503:
            # If we get a 503, then that means there is no more chat to get, the twitter space is likely over.
            return None
        chatresponse = chatrequest.json()

        return SpaceChat.ChatData(chatresponse["messages"], chatresponse["cursor"])
    
    @staticmethod
    def parseMessage(msg):
        # For Each Message, we want to Provide a readable message in our logs.
        messagekind = SpaceChat.UserActions[msg["kind"]] # Type of message sent
        messagepayload = json.loads(msg["payload"])
        messagesender = messagepayload["sender"]
        
        try:
            sender = SpaceChat.PayloadSender(messagesender["twitter_id"], messagesender["username"], messagesender["display_name"], messagesender["profile_image_url"])
            fullSenderData = f"Sender Username:{sender.sender_username} Sender Display Name: {sender.sender_display_name} Sender User ID: {sender.sender_user_id}"
        except:
            sender = SpaceChat.PayloadSenderLite(messagesender["twitter_id"])
            fullSenderData = f"Sender User ID: {sender.sender_user_id}"
            pass
       
        if messagekind == "Chat":
            messagetype = SpaceChat.RecordableActionTypes[json.loads(messagepayload["body"])["type"]]

            if messagetype == "Chat" or messagetype == "Heart" or messagetype == "ServerAudioTranscription":
                message = messagepayload["body"]
                message = json.loads(message)["body"]
                sender = SpaceChat.PayloadSender(messagesender["twitter_id"], messagesender["username"], messagesender["display_name"], messagesender["profile_image_url"])
                return f"Message: {message} {fullSenderData} Type: {messagetype}"
            
            if messagetype == "HydraControlMessage":
                message = "Hydra Control Message"
                
                # Pack the Exposed Data into their own parts
                try:
                    locale = messagesender["locale"]
                except:
                    locale = "None"
                    
                try:
                    lang = messagesender["lang"]
                except:
                    lang = "None"
                return f"{message} {fullSenderData} Sender Locale: {locale} Sender Lang: {lang} Type: {messagetype}"

            else:
                return f"{messagetype}"
                
            
        if messagekind == "Control":
            try:
                action = SpaceChat.SendableActions[messagepayload["kind"]]
            except:
                action = SpaceChat.RecordableActionTypes[messagepayload["type"]]
                
            if action != "Presence" or action != "Roster":
                try:
                    locale = messagesender["locale"]
                except:
                    locale = "None"
                    
                try:
                    lang = messagesender["lang"]
                except:
                    lang = "None"                
                return f"Action: {action} {fullSenderData}" if (locale == "None" or lang == "None") else f"Action: {action} {fullSenderData} Sender Locale: {locale} Sender Lang: {lang}"
            
        if messagekind == "Auth":
            pass
        
        else:
            return f"{messagekind}"
               
    # Get all of the chat history
    @staticmethod
    def get_chatHistory(chatvars, chatfilename="chat", path=os.getcwd()):
        chatData = SpaceChat.get_chatData(chatvars)

        chatCursor = chatData.cursor
        chatHistory = chatData.messages
        parsedMessages = list()
        messagesCollected = 0
        while chatCursor != "":
            try:
                chat_data = SpaceChat.get_chatData(chatvars, cursor=chatCursor)

                chatCursor = chat_data.cursor
                chatHistory.extend(chat_data.messages)
                
                messagesCollected += len(chat_data.messages)
                print(f"Captured {messagesCollected} Messages [Cursor: {chatCursor}] ", end="\r")
            except Exception:
                pass
        
        print("\n Finished Capturing Chat! Now Parsing...")
        parsed_messages = 0
        for raw_message in chatHistory:
            parsed_message = SpaceChat.parseMessage(raw_message)
            parsedMessages.append(parsed_message)
            parsed_messages += 1
            print(f"Parsed {parsed_messages} Messages", end="\r")
                
            
#        for message in chatHistory:
#            parsed_message = SpaceChat.parseMessage(message)
#            parsedMessages.append(parsed_message)
            
                
        with open(os.path.join(path, chatfilename + '.txt'), 'w', encoding='utf-8') as chatwriter:
            for message in parsedMessages:
                chatwriter.write(message)
                chatwriter.write('\n')
                
    def __init__(self, chat_token, chatfilename, filepath=os.getcwd()):
        self.chat_token = chat_token
        self.chatfilename = chatfilename
        self.filepath = filepath
        
        # Download the chat
        chatTokens = SpaceChat.get_tokens(self.chat_token)
        SpaceChat.get_chatHistory(chatTokens, self.chatfilename, self.filepath)
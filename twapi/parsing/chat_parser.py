
user_actions = {
        1 : "Chat", # Usual Code to represent Chat in the message logs
        2 : "Control", # User Joined/Left (Control Of The Roster)
        3 : "Auth" # This is used to get the access token for the chat (When Joining via websocket)
        }

sendable_actions = {
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
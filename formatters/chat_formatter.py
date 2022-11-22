def str_translate(original_text,dictionary_of_translations):
    """Translate String

    Args:
        original_text (str): Original Text
        dictionary_of_translations (dict): dict of translations

    Returns:
        str: translated string
    """
    out = original_text
    for keys,target in dictionary_of_translations.items():
        if keys in out:
            out = out.replace(keys, str(target))
        else:
            pass
    return out

class ChatFormatter:
    """Filename Formatter Class.
    May change to formatter class to account for chat formatting in future
    """

    @staticmethod
    def format_chat(format_string, message):
        """Parse Format String

        Args:
            format_string (str): format string
            metadata (dict): twitter space metadata

        Returns:
            str: translated string
        """

        filename_translations = {
            "%Mt": message['MessageType'],
            "%Ac": str(message['Action']),
            "%At": str(message.get("ActionType")),
            "%Si": str(message.get("MessageSender").get("user_id")),
            "%Un": str(message.get("MessageSender").get("username")),
            "%Dn": str(message.get("MessageSender").get("display_name")),
            "%Pf": str(message.get("MessageSender").get("profile_image_url")),
            "%Ul": str(message.get("MessageSender").get("locale")),
            "%Ui": str(message.get("MessageSender").get("twitter_id")),
            "%Uc": str(message.get("MessageSender").get("lang")),
            "%Mb": str(message.get("Body")),
            "%Me": str(message.get("Emoji")),
            "%Pi": str(message.get("GuestParticipantIndex")),
            "%Pu": str(message.get("GuestUsername")),
            "%Tu": str(message.get("Timestamp")),
            "%Uu": str(message.get("UUID")),
            "%Us": str(message.get("Signature")),
        }
        return str_translate(format_string, filename_translations)

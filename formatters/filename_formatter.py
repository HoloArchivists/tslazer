import datetime

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

class FilenameFormatter:
    """Filename Formatter Class.
    May change to formatter class to account for chat formatting in future
    """

    @staticmethod
    def format_filename(format_string, metadata):
        """Parse Format String

        Args:
            format_string (str): format string
            metadata (dict): twitter space metadata

        Returns:
            str: translated string
        """
        current_time = datetime.datetime.now()
        current_time_utc = datetime.datetime.utcnow()

        try:
            title = metadata["data"]["audioSpace"]["metadata"]["title"]
        except KeyError:
            # Account for Spaces that have no title
            title = f"{metadata['data']['audioSpace']['metadata']['creator_results']['result']['legacy']['name']}'s Space"

        filename_translations = {
            "%St": title,
            "%Si": str(metadata["data"]["audioSpace"]["metadata"]["rest_id"]),
            "%Ud": str(metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["name"]),
            "%Un": str(metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["screen_name"]),
            "%Ui": str(metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["rest_id"]),
            "%Sa": str(metadata["data"]["audioSpace"]["metadata"]["started_at"]),
            "%Ca": str(metadata["data"]["audioSpace"]["metadata"]["created_at"]),
            "%Ua": str(metadata["data"]["audioSpace"]["metadata"]["updated_at"]),
            "%Du": str(current_time.replace(tzinfo=datetime.timezone.utc).timestamp()),
            "%Dy": str(current_time.year),
            "%Dm": str(current_time.month),
            "%Dd": str(current_time.day),
            "%Dt": f"{current_time_utc.hour}H{current_time_utc.minute}M{current_time_utc.second}S",
            "%Dl": f"{current_time.hour}H{current_time.minute}M{current_time.second}S"
        }
        return str_translate(format_string, filename_translations)

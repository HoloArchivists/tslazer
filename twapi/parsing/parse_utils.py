import json
import logging
import os
import re
from urllib.parse import urlparse

import requests


def parse_data(path, url_data, writeinfo):
    """Parse the URL data

    Args:
        path (str): where to write the info file, if writeinfo is true
        url_data (json): url info
        writeinfo (bool): write info?
    """

    if writeinfo is True:
        with open(os.path.join(path, "playlist_urls.txt"), 'w', encoding='utf-8') as urlfile:
            urlfile.write(json.dumps(url_data, indent=4))
    location = re.sub(r"dynamic_playlist\.m3u8\?type=[a-z]*", "master_playlist.m3u8", 
                      url_data["source"]["location"]) # Handle both replays and dynamic spaces
    status = url_data["source"]["status"]
    stream_type = url_data["source"]["streamType"]
    sessionid = url_data["sessionId"]
    chat_token = url_data["chatToken"]
    share_url = url_data["shareUrl"]
    return(location, status, stream_type, sessionid, chat_token, share_url)

def parse_master_data(location):
    """Parse Master URL master Data

    Args:
        location (str): where to download the m3u8

    Returns:
        tuple: chunk location, server, source
    """
    if location.endswith("?type=replay"):
        chunk_location = re.sub(r"playlist_\d{20}\.m3u8\?type=replay", "", location)
    else:
        chunk_location = location.replace("master_playlist.m3u8", "")
    server = "https://"+urlparse(location).netloc
    if location.endswith("?type=replay"):
        source = location
    else:
        source = server + requests.get(location, timeout=10).text.split('\n')[-2]
    return (chunk_location, server, source)

def get_media_key(space_info_json):
    """Extract Twitter Space Media Key from metadata. This is used to obtain the URLs for the space.

    Args:
        space_info_json (json): Twitter Space Metadata

    Returns:
        str: Twitter Space Media Key
    """
    try:
        return space_info_json["data"]["audioSpace"]["metadata"]["media_key"]
    except KeyError:
        print("[TSLAZER] ERROR: Space Ended. Recording Unavailable.")
        logging.info("Space Ended. Terminating.")
        exit()
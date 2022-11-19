
# Initial Parse
# Extract Playlist type, Target duration, ext version

import glob  # maybe use os.path or something for universiality?
import logging
import os
import re

# Goal: Get all the chunks and create an individual URL for each
import requests


def get_m3u8(url, path):
    """Download m3u8

    Args:
        url (str): url
        path (str): path to m3u8

    Returns:
        filename: name of the downloaded m3u8
    """
    # Download M3U8s to path
    m3u8_request = requests.get(url, timeout=10)
    filename = re.search(r'[a-zA-Z]+_([A-Za-z0-9]+(\.(m3u8)+)+)', url)[0]
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as m3u8file:
        m3u8file.write(m3u8_request.text)
        logging.info("SUCCESSFULLY CREATED %s" % filename)
    return filename

def parse_m3u8(path, baseurl, filename):
    """Parse m3u8 and return the audio URLs

    Args:
        path (str): path to m3u8
        baseurl (str): base url for the audio
        filename (str): filename

    Returns:
        list: chunk urls
    """
    # Generate New URLs
    chunk_urls = list()
    with open(os.path.join(path, filename), 'r', encoding='utf-8') as m3u8file:
        for line in m3u8file.readlines():
            if not line.startswith('#EXT'):
                chunk_urls.append(baseurl + line.replace('\n', ''))
    return chunk_urls

def cleanup(path, keepm3u8):
    """Cleanup download folder after space is downloaded

    Args:
        path (str): download path
        keepm3u8 (bool): keepm3u8?
    """
    if keepm3u8 is True:
        logging.info("Keepinfo is enabled, keeping m3u8 files.")
    else:
        # Delete the m3u8s
        m3u8s = glob.glob('*.m3u8', root_dir=path)
        for m3u8 in m3u8s:
            os.remove(os.path.join(path, m3u8))
        logging.info("Removed %s m3u8 files" % len(m3u8s))
        
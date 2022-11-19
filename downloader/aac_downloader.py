import concurrent.futures
import logging
import os
import shutil
import subprocess
import uuid
from sys import platform

import mutagen.id3 as mid3
import requests
from requests_futures.sessions import FuturesSession

# AAC downloader and patcher
# Ultra Fast Downloading

def check_ffmpeg(ffmpeg_path):
    """Check if ffmpeg exists
    Only if the ffmpeglocation option in the config is a path

    Args:
        ffmpeg_path (path): path to ffmpeg
    """
    is_present = os.path.isdir(ffmpeg_path)
    if is_present is False:
        print("[TSLAZER] Missing FFMPEG or Invalid Config.")
        logging.error("Detected Invalid Config or Missing FFmpeg. Terminating Tslazer")
        exit()

def download_chunks(download_path, chunk_list):
    """Download chunks from m3u8

    Args:
        download_path (path): folder to put the space
        chunk_list (list): list of chunk urls

    Returns:
        str: string of the unique folder where the chunks reside
    """

    # Generate a folder with a UUID as the title
    # Download all the chunks (threaded)
    folderpath = os.path.join(download_path, uuid.uuid4().hex)
    os.mkdir(folderpath)
    logging.info("Generated Folder %s" % str(folderpath))

    # Prepare for ultrafast downloading
    session = FuturesSession(max_workers=os.cpu_count())

    for index, chunk in enumerate(chunk_list):
        # Replace the chunk URL with a future
        # Thank you Ryu for helping me out here.
        chunk_list[index] = (session.get(chunk_list[index]), f"chunk_{index}.aac")

    logging.info("Finished Getting %s URLs, waiting for responses" % len(chunk_list))
    concurrent.futures.wait([chunk[0] for chunk in chunk_list], timeout=5,
                            return_when=concurrent.futures.ALL_COMPLETED)
    logging.info("Retrieved All Chunks Successfully")

    for chunk in chunk_list:
        with open(os.path.join(folderpath, chunk[1]), 'wb') as chunk_writer:
            chunk_writer.write(chunk[0].result().content)
            chunk_writer.close()
    logging.info("Downloaded All Chunks Successfully")
    return folderpath


def patch_chunks(download_path, chunk_path):
    """Patch the ID3 Tags that are left over in Twitter Spaces

    Args:
        download_path (str): download path
        chunk_path (_type_): path to chunks
    """
    # Patch ID3 Bug with each chunk
    # Create a chunk index file for ffmpeg
    with open(os.path.join(download_path, "chunkindex.txt"), "w", encoding='utf-8') as index_writer:
        chunk_number = 0
        for file in os.scandir(chunk_path):
            try:
                audio = mid3.ID3(os.path.join(chunk_path, file.name))
                audio.delete(os.path.join(chunk_path, file.name))
                audio.save(os.path.join(chunk_path, file.name))
            except Exception as e:
                logging.error("Ran into Exception %s" % str(e))
                pass
            index_writer.write(f"file \'{chunk_path}/chunk_{chunk_number}.aac\'\n")
            chunk_number += 1
    logging.info("Sucessfully Patched All Chunks")

def concat_chunks(download_path, chunk_path, filename, ffmpeglocation, withmeta):
    """Use FFmpeg to create one continous audio file

    Args:
        download_path (str): download path
        chunk_path (str): chunk path
        filename (str): filename
        ffmpeglocation (str): ffmpeg location
        withmeta (bool): write metadata? (Defaults to false if downloading from master URL)
    """
    # Use FFmpeg to generate a single continous twitter space file
    # Download to a filename decided by the filename format
    if withmeta is True:
        filename = f"no_meta_{filename}"
    command = f"{ffmpeglocation} -f concat -safe 0 -i chunkindex.txt -c copy \"{filename}.m4a\" -loglevel fatal"

    if platform.startswith("linux"):
        subprocess.run(command, cwd=download_path, shell=True, check=True) #https://github.com/HoloArchivists/tslazer/issues/1
    else:
        subprocess.run(command, cwd=download_path, check=True)

    # Delete the Directory with all the chunks as we no longer need them
    shutil.rmtree(chunk_path)
    logging.info("Successfully removed temporary folder %s." % chunk_path)

    os.remove(os.path.join(download_path, "chunkindex.txt"))
    logging.info("Successfully removed chunkindex.txt.")
    logging.info("Successfully downloaded Twitter Space Audio to %s.m4a" % filename)

def download_file(url, filename, location):
    """Simple Utility Function for downloading a file

    Args:
        url (str): url to download from
        filename (str): filename to download to
        location (str): location of file
    """
    filedata = requests.get(url, stream=True, timeout=15)
    with open(os.path.join(location, filename), 'wb') as out_file:
        shutil.copyfileobj(filedata.raw, out_file)

def add_meta(metadata, download_path, filename, ffmpeglocation):
    """Add metadata to the Twitter Space

    Args:
        metadata (dict): Twitter Space metadata
        download_path (str): path to download
        filename (str): filename
        ffmpeglocation (str): ffmpeg location
    """
    # Use FFMpeg to add Metadata to the Twitter Space
    #space_id = metadata["data"]["audioSpace"]["metadata"]["rest_id"]
    title = metadata["data"]["audioSpace"]["metadata"]["title"]
    #created_at = metadata["data"]["audioSpace"]["metadata"]["created_at"]
    try:
        #creator_id = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["id"]
        creator_screen_name = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["screen_name"]
        creator_display_name = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["name"]
        creator_pfp = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["profile_image_url_https"].replace("_normal", "") # Get pfp at full size
    except KeyError:
        #creator_id = "0"
        creator_screen_name = "Protected_User"
        creator_display_name = "Protected User"
        creator_pfp = "https://abs.twimg.com/sticky/default_profile_images/default_profile.png"

    pfp_filename = f"{uuid.uuid4().hex}.jpg"
    download_file(creator_pfp, pfp_filename, download_path)

    command = f"{ffmpeglocation} -y -i \"no_meta_{filename}.m4a\" -i \"{os.path.join(download_path, pfp_filename)}\" -map 0 -map 1 -c copy -metadata title=\"{title}\" -metadata artist=\"{creator_display_name}\" -metadata composer=\"{creator_screen_name}\" -metadata comment=\"https://github.com/ef1500\" -disposition:v:0 attached_pic -loglevel fatal \"{filename}.m4a\""

    if platform.startswith("linux"):
        subprocess.run(command, cwd=download_path, shell=True, check=True) #https://github.com/HoloArchivists/tslazer/issues/1
    else:
        subprocess.run(command, cwd=download_path, check=True)

    os.remove(os.path.join(download_path, pfp_filename))
    os.remove(os.path.join(download_path, f"no_meta_{filename}.m4a"))
    logging.info("Successfully added metadata to the file")
    logging.info("Successfully removed audio file with no metadata")

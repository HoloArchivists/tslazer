# tslazer.py
# Author: ef1500

import os
import re
import uuid
import time
import shutil
import requests
import subprocess
import collections
import concurrent.futures
import mutagen.id3 as mid3
from sys import platform
from datetime import datetime,timezone
import urllib.parse
import json

import WebSocketHandler
from Cookie import Cookie

from slugify import slugify
from threading import Thread
from dataclasses import dataclass
from urllib.parse import urlparse
from requests_futures.sessions import FuturesSession


class TwitterSpace:
    TwitterUser = collections.namedtuple('TwitterUser', ['name', 'screen_name', 'id'])
    
    @dataclass
    class SpacePlaylists:
        chunk_server: str
        dyn_url: str
        master_url: str
        chatToken: str
        raw_response: str
    
    @dataclass
    class Chunk:
        url: str
        filename: str
    
    @staticmethod
    def getUser(username):
        """
        Get Twitter User ID
        
        :param username: A Twitter User's @ handle
        :returns: TwitterUser NamedTuple
        """
        dataRequest = requests.get(f"https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names={username}")
        dataResponse = dataRequest.json()
        return TwitterSpace.TwitterUser(dataResponse[0]['name'], dataResponse[0]['screen_name'], dataResponse[0]['id'])
    
    @staticmethod
    def getGuestToken():
        """
        Generate a guest token for use with the Twitter API. Note: Twitter will get mad if you call this too many times
        
        :returns: string
        """
        headers = {"authorization" : "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"}
        tokenRequest = requests.post("https://api.twitter.com/1.1/guest/activate.json", headers=headers)
        tokenResponse = tokenRequest.json()
        return tokenResponse["guest_token"]
    
    @staticmethod
    def getPlaylists(media_key=None, guest_token=None, dyn_url=None, write_info=False):
        """
        Get The master playlist from a twitter space.
        
        :param media_key: The media key to the twitter space. Given in the metadata
        :param guest_token: The Guest Token that allows us to use the Twitter API without OAuth
        :param dyn_url: The dynamic/Master URL (If needed)
        :param write_info: Whether or not to write the twitter space information to a file
        :returns: NamedTuple SpacePlaylists
        """
        
        dataResponse = None
        
        if media_key != None and guest_token != None:
            headers = {"authorization" : "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA", "x-guest-token" : guest_token}
            dataRequest = requests.get(f"https://twitter.com/i/api/1.1/live_video_stream/status/{media_key}", headers=headers)
            dataResponse = dataRequest.json()
            dataLocation = dataResponse['source']['location']
            dataLocation = re.sub(r"(dynamic_playlist\.m3u8((?=\?)(\?type=[a-z]{4,}))?|master_playlist\.m3u8(?=\?)(\?type=[a-z]{4,}))", "master_playlist.m3u8", dataLocation)
            
            chatToken = dataResponse["chatToken"]
            
        if dyn_url != None:
            dataLocation = dyn_url
            dataLocation = re.sub(r"(dynamic_playlist\.m3u8((?=\?)(\?type=[a-z]{4,}))?|master_playlist\.m3u8(?=\?)(\?type=[a-z]{4,}))", "master_playlist.m3u8", dataLocation)
            chatToken = "None"
        
        dataComponents = urlparse(dataLocation)
        
        # Prepare Data Path and Data Server
        # The data path is used to retrieve the True Master Playlist
        dataServer = f"{dataComponents.scheme}://{dataComponents.hostname}"
        dataPath = dataComponents.path
        
        # Get the Master Playlist
        playlistRequest = requests.get(f"{dataServer}{dataPath}")
        playlistResponse = playlistRequest.text.split('\n')[-2]
        playlistUrl = f"{dataServer}{playlistResponse}"
        
        chunkServer = f"{dataServer}{dataPath[:-20]}"
#        return TwitterSpace.SpacePlaylists(chunkServer, f"{dataServer}{dataPath}" , playlistUrl, chatToken)

        if playlistResponse == "#EXT-X-ENDLIST":
            return TwitterSpace.SpacePlaylists(chunkServer[:-14], f"{dataServer}{dataPath}" , f"{dataServer}{dataPath}", chatToken, dataResponse)
        else:
            return TwitterSpace.SpacePlaylists(chunkServer, f"{dataServer}{dataPath}" , playlistUrl, chatToken, dataResponse)
    
    @staticmethod
    def getPlaylistsWithCookie(media_key=None, cookies=None, dyn_url=None):
        """
        Use Cookies to retrieve the playlists

        Args:
            media_key (str, optional): Media Key. Defaults to None.
            cookies (dict, optional): Cookies. Defaults to None.
            dyn_url (_type_, optional): Dynamic URL. Defaults to None.
        """
        
        dataResponse = None

        if media_key != None and cookies != None:
            cookie_header = Cookie.getHeader(cookies=cookies)
            headers = {
                "authorization" : "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA", 
                "x-csrf-token" : cookies['ct0'],
                "cookie": cookie_header
            }

            dataRequest = requests.get(f"https://twitter.com/i/api/1.1/live_video_stream/status/{media_key}", headers=headers, cookies=cookies)
            dataResponse = dataRequest.json()
            dataLocation = dataResponse['source']['location']
            dataLocation = re.sub(r"(dynamic_playlist\.m3u8((?=\?)(\?type=[a-z]{4,}))?|master_playlist\.m3u8(?=\?)(\?type=[a-z]{4,}))", "master_playlist.m3u8", dataLocation)
            
            chatToken = dataResponse["chatToken"]
            
        if dyn_url != None:
            dataLocation = dyn_url
            dataLocation = re.sub(r"(dynamic_playlist\.m3u8((?=\?)(\?type=[a-z]{4,}))?|master_playlist\.m3u8(?=\?)(\?type=[a-z]{4,}))", "master_playlist.m3u8", dataLocation)
            chatToken = "None"
        
        dataComponents = urlparse(dataLocation)
        
        # Prepare Data Path and Data Server
        # The data path is used to retrieve the True Master Playlist
        dataServer = f"{dataComponents.scheme}://{dataComponents.hostname}"
        dataPath = dataComponents.path
        
        # Get the Master Playlist
        playlistRequest = requests.get(f"{dataServer}{dataPath}")
        playlistResponse = playlistRequest.text.split('\n')[-2]
        playlistUrl = f"{dataServer}{playlistResponse}"
        
        chunkServer = f"{dataServer}{dataPath[:-20]}"
#        return TwitterSpace.SpacePlaylists(chunkServer, f"{dataServer}{dataPath}" , playlistUrl, chatToken)
        if playlistResponse == "#EXT-X-ENDLIST":
            return TwitterSpace.SpacePlaylists(chunkServer[:-14], f"{dataServer}{dataPath}" , f"{dataServer}{dataPath}", chatToken, dataResponse)
        else:
            return TwitterSpace.SpacePlaylists(chunkServer, f"{dataServer}{dataPath}" , playlistUrl, chatToken, dataResponse)
    
    @staticmethod
    def getMetadata(space_id, guest_token):
        """
        Retrieve the Metadata for a given twitter space ID or URL.
        Note: If you are working with a dynamic url, then you cannot use this function.
        
        :param space_id: URL or Space ID
        :param guest_token: Guest Token
        """
        spaceID = self.getSpaceId(space_id)
            
        # Prepare Variables
        headers = {"authorization" : "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA", "x-guest-token" : guest_token}
        variables = f"{{\"id\": \"{spaceID}\",\"isMetatagsQuery\":true,\"withSuperFollowsUserFields\":true,\"withDownvotePerspective\":false,\"withReactionsMetadata\":false,\"withReactionsPerspective\":false,\"withSuperFollowsTweetFields\":true,\"withReplays\":true}}"
        features = "{\"dont_mention_me_view_api_enabled\":true,\"interactive_text_enabled\":true,\"responsive_web_uc_gql_enabled\":false,\"vibe_tweet_context_enabled\":false,\"responsive_web_edit_tweet_api_enabled\":false,\"standardized_nudges_for_misinfo_nudges_enabled\":false}"
        
        metadataRequest = requests.get(f"https://twitter.com/i/api/graphql/yMLYE2ltn1nOZ5Gyk3JYSw/AudioSpaceById?variables={variables}&features={features}", headers=headers)
        metadataResponse = metadataRequest.json()
        
        return metadataResponse
    
    @staticmethod
    def getMetadataWithCookies(space_id: str,  cookies: dict[str,str]):
        space_id = TwitterSpace.getSpaceId(space_id)

        cookie_header = Cookie.getHeader(cookies=cookies)
        headers = {
            "authorization" : "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA", 
            "x-csrf-token" : cookies['ct0'],
            "cookie": cookie_header
        }  

        variables = {
            "id": space_id,
            "isMetatagsQuery": True,
            "withReplays": True,
            "withListeners": True
        }

        features = {
            "spaces_2022_h2_clipping": True,
            "spaces_2022_h2_spaces_communities": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": False,
            "tweet_awards_web_tipping_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_media_download_video_enabled": False,
            "responsive_web_enhance_cards_enabled": False
        }

        encoded_variables = urllib.parse.quote(json.dumps(variables, indent=None, separators=(",", ":")))
        encoded_features = urllib.parse.quote(json.dumps(features, indent=None, separators=(",", ":")))

        url = f"https://twitter.com/i/api/graphql/xVEzTKg_mLTHubK5ayL0HA/AudioSpaceById?variables={encoded_variables}&features={encoded_features}"

        metadataRequest = requests.get(url, headers=headers, cookies=cookies)
        metadataResponse = metadataRequest.json()
        
        return metadataResponse
    
    @staticmethod
    def getSpaceId(space_id) -> str:
        try:
            return re.findall(r"\d[a-zA-Z]{12}", space_id)[0]
        except Exception:
            print("Unable to find a space ID, please try again.")

    @staticmethod
    def getChunks(playlists):
        """
        When we recieve the chunks from the server, we want to be able to parse that m3u8 and get all of the chunks from it.
        
        :param playlists: space playlist namedtuple
        :returns: list of all chunks
        """
        try:
            playlists = TwitterSpace.getPlaylists(dyn_url=playlists.dyn_url)
        except Exception:
            pass
        
        m3u8Request = requests.get(playlists.master_url)
        m3u8Data = m3u8Request.text
        chunkList = list()
        del m3u8Request
        
        for chunk in re.findall(r"chunk_\d{19}_\d+_a\.aac", m3u8Data):
            chunkList.append(TwitterSpace.Chunk(f"{playlists.chunk_server}{chunk}", chunk))
        return chunkList    

    @staticmethod
    def downloadChunks(chunklist, filename, path=os.getcwd(), metadata=None):
        """
        Download all of the chunks from the m3u8 to a specified path.
        
        :param chunklist: list of chunks
        :param filename: Name of the file we want to write the data to
        :param path: the path to download the chunks to
        :param metadata: any additional metadata that we would like to write to the m4a 
        :returns: None
        """
        # Check if the path exists
        uniqueFoldername = str(uuid.uuid4().hex) # Create A Unique Folder Name for the Program to operate in
        if os.path.isdir(path) != True:
            os.makedirs(path) # Do I even need this?
            
        if os.path.isdir(os.path.join(path, uniqueFoldername)) != True:
            os.makedirs(os.path.join(path, uniqueFoldername))
        chunkpath = os.path.join(path, uniqueFoldername)
        
        # Get the amount of working threads that the machine has so we know how many to use
        session = FuturesSession(max_workers=os.cpu_count())
        
        for chunk in chunklist:
            # Replace the chunk url with a future
            chunk.url = session.get(chunk.url)
        print("Finished Getting URLs, Waiting for responses")
        concurrent.futures.wait([fchunk.url for fchunk in chunklist], timeout=5, return_when=concurrent.futures.ALL_COMPLETED)
        
        for chunk in chunklist:
            with open(os.path.join(chunkpath, chunk.filename), "wb") as chunkWriter:
                chunkWriter.write(chunk.url.result().content)
            del chunkWriter
                
        print("Finished Downloading Chunks")
                
        # Once we've downloaded all of the chunks, we want to make a file that ffmpeg can work with.
        with open(os.path.join(path, "chunkindex.txt"), "w+") as chunkIndexWriter:
            for file in os.scandir(chunkpath):
                # Get rid of all of the pesky id3 tags that we DONT NEED
                # Note: If the space has already ended, sometimes the ID3 Tags are gone, as
                # The HydraControlMessages are only used during a live space and are cleaned
                # After the space has ended.
                audio = mid3.ID3(os.path.join(chunkpath, file.name))
                audio.delete(os.path.join(chunkpath, file.name))
                audio.save(os.path.join(chunkpath, file.name))
                
                chunkIndexWriter.write(f"file \'./{uniqueFoldername}/{file.name}\'\n")
        
        # So we have a file now. We need execute it with ffmpeg in order to complete the download.
        if metadata == None:
            try:
                command = [
                    "ffmpeg",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    "chunkindex.txt",
                    "-c",
                    "copy",
                    f"{filename}.m4a",
                    "-loglevel",
                    "fatal"
                ]
                
                subprocess.run(command, cwd=path, check=True)

                # Delete the Directory with all of the chunks. We no longer need them.
                shutil.rmtree(chunkpath)
                os.remove(os.path.join(path, "chunkindex.txt"))
            except Exception:
                print("Failed To Create Subprocess.")
        
        if metadata != None:
            try:
                title = metadata["title"]
                author = metadata["author"]
                composer = metadata["composer"]
                pfp_location = metadata["profile_picture"]

                command = f"ffmpeg -f concat -safe 0 -i chunkindex.txt -c copy \"nometa_{filename}.m4a\" -loglevel fatal"
                add_pfp_command = f"ffmpeg -y -i \"nometa_{filename}.m4a\" -i \"{pfp_location}\" -map 0 -map 1 -c copy -metadata title=\"{title}\" -metadata artist=\"{author}\" -metadata composer=\"{composer}\" -metadata comment=\"https://github.com/ef1500\" -disposition:v:0 attached_pic \"{filename}.m4a\" -loglevel fatal"

                if platform == "linux" or platform == "linux2":  
                    subprocess.run(command, cwd=path, shell=True) # https://github.com/HoloArchivists/tslazer/issues/1
                    subprocess.run(add_pfp_command, cwd=path, shell=True)
                else:
                    subprocess.run(command, cwd=path)
                    subprocess.run(add_pfp_command, cwd=path, shell=True)
                # Delete the Directory with all of the chunks. We no longer need them.
                shutil.rmtree(chunkpath)
                os.remove(os.path.join(path, "chunkindex.txt"))
                os.remove(os.path.join(path, f"nometa_{filename}.m4a"))
                os.remove(pfp_location)
            except Exception as e:
                print("Failed To Create Subprocess.")
                return

            print(f"Successfully Downloaded Twitter Space {filename}.m4a")
            
    def _download_playlist(self):
        """
        Download the m3u8's to the specified path if the keepm3u8 argument is true
        """
        m3u8_request = requests.get(self.playlists.master_url, timeout=10)
        filename = re.search(r'[a-zA-Z]+_([A-Za-z0-9]+(\.(m3u8)+)+)', self.playlists.master_url)[0]
        with open(os.path.join(self.path, filename), 'w', encoding='utf-8') as m3u8file:
            m3u8file.write(m3u8_request.text)
            
    def _write_info(self):
        """
        Write the raw space information to a file if the writeinfo argument is true
        """
        with open(os.path.join(self.path, "playlist_urls.txt"), 'w', encoding='utf-8') as urlfile:
            urlfile.write(json.dumps(self.playlists.raw_response, indent=4))
            
    def _display_banner(self):
        banner = """
  _______  _                        
 |__   __|| |                       
    | |___| |     __ _ _______ _ __ 
    | / __| |    / _` |_  / _ \ '__|
    | \__ \ |___| (_| |/ /  __/ |   
    |_|___/______\__,_/___\___|_|   

    Record Twitter Spaces!

    Developed By EF1500 | Holoarchivists
    https://github.com/ef1500 | https://github.com/HoloArchivists
        """
        print(banner)
        
    def _display_info(self):
        """
        Display the Twitter Space information on the screen
        """
        space_information = ["[TWITTER SPACE STREAM INFORMATION]"]
        if self.space_id:
            space_information.append(f"Twitter Space ID: {self.space_id}")
        if self.dyn_url:
            space_information.append(f"Dynamic URL: {self.dyn_url}")
        space_information.append(f"Master URL: {self.playlists.master_url}")
        space_information.append(f"Chat Token: {self.playlists.chatToken}")

        if self.metadata:
            space_information.extend([
                "\n[TWITTER SPACE METADATA]",
                f"Title: {self.title}",
                f"Current State: {self.state}",
                f"Created At: {self.created_at}",
                f"Started At: {self.started_at}",
                f"Media Key: {self.media_key}",
                "\n[TWITTER SPACE CREATOR INFO]",
                f"Screen Name: {self.creator.screen_name}",
                f"Display Name: {self.creator.name}",
                f"ID: {self.creator.id}"
            ])
        
        print('\n'.join(space_information))
            
    def __init__(self, space_id=None, dyn_url=None, filename=None, filenameformat=None, path=None, withChat=False, cookiesPath=None, keepm3u8=False, write_info=False):
        self.space_id = space_id
        self.dyn_url = dyn_url
        self.filename = filename
        self.filenameformat = filenameformat
        self.path = path
        self.cookiesPath = cookiesPath
        self.metadata = None
        self.playlists = None
        self.wasrunning = False
        self.keepm3u8 = keepm3u8
        self.write_info = write_info
        
        self._display_banner()

        # If no cookiesPath provided, get guest_token
        cookies, guest_token = None, None
        if self.cookiesPath is not None:
            reader = Cookie(file_path=self.cookiesPath)
            cookies = reader.getCookies(reader)
        else:
            guest_token = TwitterSpace.getGuestToken()

        # If space_id is provided, get metadata
        if self.space_id is not None:
            self.metadata = TwitterSpace.getMetadata(self.space_id, guest_token) if guest_token else TwitterSpace.getMetadataWithCookies(self.space_id, cookies)
            
        # If there's metadata, set the metadata.
        if self.metadata != None:
            
            try:
                self.title = self.metadata['data']['audioSpace']['metadata']['title']
            except Exception:
                self.title = self.metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["screen_name"].__add__("\'s space") # IF We couldn't get the space Title, just use twitter's default here.
                
            self.media_key = self.metadata["data"]["audioSpace"]["metadata"]["media_key"]
            self.state = self.metadata["data"]["audioSpace"]["metadata"]["state"]
            self.created_at = self.metadata["data"]["audioSpace"]["metadata"]["created_at"]
            self.started_at = self.metadata["data"]["audioSpace"]["metadata"]["started_at"]
            self.updated_at = self.metadata["data"]["audioSpace"]["metadata"]["updated_at"]
            try:
                self.creator = TwitterSpace.TwitterUser(self.metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["name"], self.metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["screen_name"], self.metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["rest_id"])
            except KeyError:
                self.creator = TwitterSpace.TwitterUser("Protected_User", "Protected", "0")
                
            try:
                self.creator_pfp = self.metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["profile_image_url_https"].replace("_normal", "") # Get pfp at full size
            except KeyError:
                self.creator_pfp = "https://abs.twimg.com/sticky/default_profile_images/default_profile.png"
                
            pfp_filename = f"{uuid.uuid4().hex}.jpg"
            
            filedata = requests.get(self.creator_pfp, stream=True, timeout=15)
            with open(os.path.join(self.path, pfp_filename), 'wb') as out_file:
                shutil.copyfileobj(filedata.raw, out_file)
                
        # Get the Fileformat here, so that way it won't hinder the chat exporter when it's running.
        # Now let's format the fileformat per the user's request.
        # File Format Options:
        #    %Ud	Host Display Name
        #    %Un	Host Username
        #    %Ui	Host User ID
        #    %St	Space Title
        #    %Si	Space ID
        #    %Dy    Year
        #    %Dm    Month
        #    %Dd    Day
        #    %Dt    Time (Utc)
        #    %Dl    Time (Local)
        if self.filenameformat != None and self.metadata != None:
            self.filenameformat = self.filenameformat.replace("%Ud", self.creator.name)
            self.filenameformat = self.filenameformat.replace("%Un", self.creator.screen_name)
            self.filenameformat = self.filenameformat.replace("%Ui", self.creator.id)
            self.filenameformat = self.filenameformat.replace("%St", self.title)
            self.filenameformat = self.filenameformat.replace("%Si", self.space_id)
            datelocal = datetime.now()
            day, year, month, hour, minute, second = datelocal.day, datelocal.year, datelocal.month, datelocal.hour, datelocal.minute, datelocal.second
            dateutc = datetime.now(timezone.utc)
            houru, minuteu, secondu = dateutc.hour, dateutc.minute, dateutc.second            
            self.filenameformat = self.filenameformat.replace("%Dy", f"{year}")
            self.filenameformat = self.filenameformat.replace("%Dd", f"{day}")
            self.filenameformat = self.filenameformat.replace("%Dm", f"{month}")
            self.filenameformat = self.filenameformat.replace("%Dt", f"{houru}-{minuteu}-{secondu}")
            self.filenameformat = self.filenameformat.replace("%Dl", f"{hour}-{minute}-{second}")
            self.filenameformat = slugify(self.filenameformat, allow_unicode=True, lowercase=False, separator='_')
            
        # Now lets get the playlists
        if space_id != None and self.metadata != None:
            if self.cookiesPath == None:
                self.playlists = TwitterSpace.getPlaylists(media_key=self.media_key, guest_token=guest_token)
            else:
                self.playlists =TwitterSpace.getPlaylistsWithCookie(media_key=self.media_key, cookies=cookies)
        if space_id == None and self.metadata == None:
            if self.cookiesPath == None:
                self.playlists = TwitterSpace.getPlaylists(dyn_url=self.dyn_url)
            else:
                self.playlists =TwitterSpace.getPlaylistsWithCookie(dyn_url=self.dyn_url, cookies=cookies)
                
        self._display_info()
        
        if self.write_info is True:
            self._write_info()
            
        if self.keepm3u8 is True:
            self._download_playlist()
            
        # Now Start a subprocess for running the chat exporter
        if withChat == True and self.metadata != None:
            print("[ChatExporter] Chat Exporting is currently only supported for Ended Spaces with a recording. To Export Chat for a live space, copy the chat token and use WebSocketDriver.py.")
            chatThread = Thread(target=WebSocketHandler.SpaceChat, args=(self.playlists.chatToken, self.filenameformat, self.path,))
            #chatThread.start()
            
        # Print out the Space Information and wait for the Space to End (if it's running)             
        if self.metadata != None and self.state == "Running":
            self.wasrunning = True
            # Print out the space Information
            print(f"[TSLAZER] VALID SPACE DETECTED")
            print("[TSLAZER] Waiting for space to end...")
            while self.state == "Running":
                if self.cookiesPath == None:
                    self.metadata = TwitterSpace.getMetadata(self.space_id, guest_token)
                else:
                    self.metadata = TwitterSpace.getMetadataWithCookies(self.space_id, cookies)
                try:
                    self.state = self.metadata["data"]["audioSpace"]["metadata"]["state"]
                    time.sleep(10)
                except Exception:
                    self.state = "ERROR"
            print("Space Ended. Now Downloading...")
            
        # Check to see if the master playlist is avaliable yet (https://github.com/HoloArchivists/tslazer/issues/5)
        if self.wasrunning is True:
            print(f"[TSLAZER] Checking Master Playlist Availability")
            check_request = requests.get(self.playlists.master_url, timeout=5)
            if check_request.status_code != 200:
                print(f"[TSLAZER] Master Playlist Not Available Yet.")
                print(f"[TSLAZER] Checking Master Playlist Availability Every 10 Seconds...")

                attempts = 1
                while attempts <= 100 and check_request.status_code != 200:
                    time.sleep(10)
                    check_request = requests.get(self.playlists.master_url, timeout=5)
                    attempts += 1

#        if self.metadata != None and self.state == "Ended" and self.wasrunning == False:
#            try:
            # Print out the space Information
#                print(f"Space Has Finished and Recording was found!")
#                if self.withChat == True:
#                    chatThread.start() # If We're Downloading a Recording, we're all good to download the chat.
#                print("[ChatExporter]: Chat Thread Started")
#            except Exception:
#                print("Space Ended and Unable to get master url.")
            
        # Now it's time to download.        
        if self.metadata == None:
            chunks = TwitterSpace.getChunks(self.playlists)
            TwitterSpace.downloadChunks(chunks, self.filename, path=self.path)
        
        if self.metadata != None:
            m4aMetadata = {"title" : self.title, "author" : self.creator.screen_name, "composer": self.creator.name, "profile_picture": os.path.join(self.path, pfp_filename)}
            if self.cookiesPath == None:
                self.playlists.master_url = TwitterSpace.getPlaylists(dyn_url=self.playlists.dyn_url).master_url
            else:
                self.playlists.master_url = TwitterSpace.getPlaylistsWithCookie(dyn_url=self.playlists.dyn_url, cookies=cookies).master_url
            livechunks = TwitterSpace.getChunks(self.playlists)
            TwitterSpace.downloadChunks(livechunks, self.filenameformat, self.path, m4aMetadata)
 #           spaceThread = Thread(target=TwitterSpace.downloadChunks, args=(chunks, self.filenameformat, self.path, m4aMetadata,))
#            spaceThread.start()
            
        if self.metadata != None and self.state == "Ended" and withChat == True and self.wasrunning == False:
            chatThread.start() # If We're Downloading a Recording, we're all good to download the chat.
            print("[ChatExporter]: Chat Thread Started")

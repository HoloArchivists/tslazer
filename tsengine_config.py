import downloader.aac_downloader as aac_downloader
import downloader.m3u8_parser as m3u8_parser
import formatters.filename_formatter as filename_formatter
import prettifiers.cli as cli_prettifier
import twapi.auth.get_space as get_space
import twapi.auth.get_urls as get_urls
import twapi.guest.get_space_guest as get_space_guest
import twapi.guest.get_guest_token as get_guest_token
import twapi.guest.get_urls_guest as get_urls_guest
import twapi.parsing.parse_utils as parse_utils
import utils.config_utils as config_utils
import utils.soft_slugify as soft_slugify
import twapi.space_utils as space_utils
import twapi.user_utils as user_utils
import videoutils.video_generator as video_generator
import os
import uuid
import logging


# Config Based Downloading
def download_from_config(config_file, space_id=None, dynamic_url=None, user_id=None, screen_name=None, output_filename=None):

    try:
        config = config_utils.open_config(config_file)
    except FileNotFoundError:
        print("[TSLAZER] UNABLE TO LOCATE CONFIG FILE")

    banner = open(config["cliconfig"]["banner"], 'r', encoding='utf-8')
    banner = banner.read()
    print(banner)
    download_path = config["dlconfig"]["dlpath"]

    if dynamic_url and output_filename is not None:
        #Download Twitter Space from Master URL
        print(f"[TSLAZER] ATTEMPTING TO DOWNLOAD SPACE FROM MASTER URL TO {output_filename}.m4a")
        print("[TSLAZER] WARNING: DOWNLOADING AN ONGOING SPACE FROM A DYNAMIC/MASTER URL WILL RESULT IN INCOMPLETE DOWNLOADS")
        try:
            master_data = parse_utils.parse_master_data(dynamic_url)
            m3u8_file = m3u8_parser.get_m3u8(master_data[2], download_path)
        except Exception:
            logging.error("m3u8 is no longer avaliable")
            print("[TSLAZER] M3U8 FILE IS NO LONGER AVALIABLE OR INVALID LINK.")
            exit()
        chunk_urls = m3u8_parser.parse_m3u8(download_path, master_data[0], m3u8_file)
        downloaded_chunks = aac_downloader.download_chunks(download_path, chunk_urls)
        filename = soft_slugify.soft_slugify(output_filename)
        aac_downloader.patch_chunks(download_path, downloaded_chunks)
        aac_downloader.concat_chunks(download_path,downloaded_chunks,
                                    filename, config["dlconfig"]["ffmpeglocation"], False)
        logging.warning("Ignoring withmeta option in config.toml, defaulting to false")
        # Withmeta must be False by default here
        m3u8_parser.cleanup(download_path, config["dlconfig"]["keepm3u8"])

    if user_id is not None and config["auth"]["user"] is True:
        if config["auth"]["user"] is False:
            print("[TSLAZER] You are attempting to perform an action which cannot be done via Twitter's guest API.")
        print(f"[TSLAZER] RESOLVING SPACE FROM USER ID {user_id}")
        space_id = space_utils.check_user(user_id, config["auth"]["authtoken"], 
                                          config["auth"]["cookies"])
        if space_id is None:
            print("[TSLAZER] Specified user is not currently hosting a space.")
            exit()

    if screen_name is not None and config["auth"]["user"] is True:
        print(f"[TSLAZER] RESOLVING SPACE FROM SCREEN NAME {screen_name}")
        user_id = user_utils.get_user_id(screen_name)
        space_id = space_utils.check_user(user_id, config["auth"]["authtoken"], 
                                          config["auth"]["cookies"])
        if space_id is None:
            print("[TSLAZER] Specified user is not currently hosting a space.")
            exit()
            
    if config["auth"]["user"] is False and space_id is not None:
        print(f"[TSLAZER] ATTEMPTING TO DOWNLOAD SPACE FROM SPACE ID {space_id} using Twitter Guest API")
        guest_token = get_guest_token.get_guest_token()
        sp = get_space_guest.get_space_guest(space_id, guest_token)
        media_key = parse_utils.get_media_key(sp)
        data = get_urls_guest.get_data_guest(media_key, guest_token)
        more_data = parse_utils.parse_data(download_path, data, config["dlconfig"]["writeinfo"])
        get_space_guest.wait_for_end_guest(space_id, sp, guest_token)
        master_data = parse_utils.parse_master_data(more_data[0])
        cli_prettifier.prettify_metadata(sp)
        cli_prettifier.prettify_urls(more_data[0], master_data[2],
                                    more_data[1], more_data[2], more_data[-1])
        m3u8_file = m3u8_parser.get_m3u8(master_data[2], download_path)
        chunk_urls = m3u8_parser.parse_m3u8(download_path, master_data[0], m3u8_file)
        downloaded_chunks = aac_downloader.download_chunks(download_path, chunk_urls)
        aac_downloader.patch_chunks(download_path, downloaded_chunks)
        filename = soft_slugify.soft_slugify(
            filename_formatter.FilenameFormatter.format_filename(config["dlconfig"]["format"], sp))
        aac_downloader.concat_chunks(download_path,
                                     downloaded_chunks, filename, 
                                     config["dlconfig"]["ffmpeglocation"],
                                     config["dlconfig"]["withmeta"])
        if config["dlconfig"]["withmeta"] is True:
            aac_downloader.add_meta(sp, download_path, filename,
                                    config["dlconfig"]["ffmpeglocation"])
        m3u8_parser.cleanup(download_path, config["dlconfig"]["keepm3u8"])

    if space_id is not None and config["auth"]["user"] is True:

        print(f"[TSLAZER] ATTEMPTING TO DOWNLOAD SPACE FROM SPACE ID {space_id}")
        sp = get_space.get_space(space_id, config["auth"]["authtoken"],
                                config["auth"]["crsftoken"], config["auth"]["cookies"])
        media_key = parse_utils.get_media_key(sp)
        data = get_urls.get_data(media_key, config["auth"]["authtoken"], config["auth"]["cookies"])
        more_data = parse_utils.parse_data(download_path, data, config["dlconfig"]["writeinfo"])
        get_space.wait_for_end(space_id, sp, config["auth"]["authtoken"],
                            config["auth"]["crsftoken"], config["auth"]["cookies"])
        master_data = parse_utils.parse_master_data(more_data[0])
        cli_prettifier.prettify_metadata(sp)
        cli_prettifier.prettify_urls(more_data[0], master_data[2],
                                    more_data[1], more_data[2], more_data[-1])
        m3u8_file = m3u8_parser.get_m3u8(master_data[2], download_path)
        chunk_urls = m3u8_parser.parse_m3u8(download_path, master_data[0], m3u8_file)
        downloaded_chunks = aac_downloader.download_chunks(download_path, chunk_urls)
        aac_downloader.patch_chunks(download_path, downloaded_chunks)
        filename = soft_slugify.soft_slugify(
            filename_formatter.FilenameFormatter.format_filename(config["dlconfig"]["format"], sp))
        aac_downloader.concat_chunks(download_path,
                                     downloaded_chunks, filename, 
                                     config["dlconfig"]["ffmpeglocation"],
                                     config["dlconfig"]["withmeta"])
        if config["dlconfig"]["withmeta"] is True:
            aac_downloader.add_meta(sp, download_path, filename,
                                    config["dlconfig"]["ffmpeglocation"])
        m3u8_parser.cleanup(download_path, config["dlconfig"]["keepm3u8"])
        
    if config["dlconfig"]["generatevideo"] is True and space_id is not None:
        creator_pfp = sp["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["profile_image_url_https"].replace("_normal", "")
        pfp_filename = f"{uuid.uuid4().hex}.jpg"
        aac_downloader.download_file(creator_pfp, pfp_filename, download_path)
        
        video_generator.generate_template(os.path.join(download_path, f"{filename}.m4a"), os.path.join(download_path, pfp_filename), download_path)
        video_generator.generate_video(config["dlconfig"]["ffmpeglocation"], f"{filename}.m4a", filename, download_path)
        
        #cleanup
        os.remove(os.path.join(download_path, pfp_filename))
        os.remove(os.path.join(download_path, "generated_template.png"))
        
def download_from_cli(guestmode=True, authtoken=None, crsftoken=None, cookies=None, withmeta=True, writeinfo=False, keepm3u8=False, generatevideo=False, format_str="%%St-%%Si-%%Ud-%%Un", 
                      ffmpeglocation="ffmpeg", dlpath=os.getcwd(), space_id=None, dynamic_url=None, user_id=None, screen_name=None, output_filename=None):
    
    banner = open("./prettifiers/banner.txt", 'r', encoding='utf-8')
    banner = banner.read()
    print(banner)
    download_path = dlpath
    
    if dynamic_url and output_filename is not None:
        #Download Twitter Space from Master URL
        print(f"[TSLAZER] ATTEMPTING TO DOWNLOAD SPACE FROM MASTER URL TO {output_filename}.m4a")
        print("[TSLAZER] WARNING: DOWNLOADING AN ONGOING SPACE FROM A DYNAMIC/MASTER URL WILL RESULT IN INCOMPLETE DOWNLOADS")
        try:
            master_data = parse_utils.parse_master_data(dynamic_url)
            m3u8_file = m3u8_parser.get_m3u8(master_data[2], download_path)
        except Exception:
            logging.error("m3u8 is no longer avaliable")
            print("[TSLAZER] M3U8 FILE IS NO LONGER AVALIABLE OR INVALID LINK.")
            exit()
        chunk_urls = m3u8_parser.parse_m3u8(download_path, master_data[0], m3u8_file)
        downloaded_chunks = aac_downloader.download_chunks(download_path, chunk_urls)
        filename = soft_slugify.soft_slugify(output_filename)
        aac_downloader.patch_chunks(download_path, downloaded_chunks)
        aac_downloader.concat_chunks(download_path,downloaded_chunks,
                                    filename, ffmpeglocation, False)
        logging.warning("Ignoring withmeta option in config.toml, defaulting to false")
        # Withmeta must be False by default here
        m3u8_parser.cleanup(download_path, keepm3u8)
        
    if user_id is not None and guestmode is False:
        print(f"[TSLAZER] RESOLVING SPACE FROM USER ID {user_id}")
        space_id = space_utils.check_user(user_id, authtoken,cookies)
        if space_id is None:
            print("[TSLAZER] Specified user is not currently hosting a space.")
            exit()
            
    if screen_name is not None and guestmode is False:
        print(f"[TSLAZER] RESOLVING SPACE FROM SCREEN NAME {screen_name}")
        user_id = user_utils.get_user_id(screen_name)
        space_id = space_utils.check_user(user_id, authtoken,cookies)
        if space_id is None:
            print("[TSLAZER] Specified user is not currently hosting a space.")
            exit()
            
    if guestmode is True and space_id is not None:
        print(f"[TSLAZER] ATTEMPTING TO DOWNLOAD SPACE FROM SPACE ID {space_id} using Twitter Guest API")
        guest_token = get_guest_token.get_guest_token()
        sp = get_space_guest.get_space_guest(space_id, guest_token)
        media_key = parse_utils.get_media_key(sp)
        data = get_urls_guest.get_data_guest(media_key, guest_token)
        more_data = parse_utils.parse_data(download_path, data, writeinfo)
        get_space_guest.wait_for_end_guest(space_id, sp, guest_token)
        master_data = parse_utils.parse_master_data(more_data[0])
        cli_prettifier.prettify_metadata(sp)
        cli_prettifier.prettify_urls(more_data[0], master_data[2],
                                    more_data[1], more_data[2], more_data[-1])
        m3u8_file = m3u8_parser.get_m3u8(master_data[2], download_path)
        chunk_urls = m3u8_parser.parse_m3u8(download_path, master_data[0], m3u8_file)
        downloaded_chunks = aac_downloader.download_chunks(download_path, chunk_urls)
        aac_downloader.patch_chunks(download_path, downloaded_chunks)
        filename = soft_slugify.soft_slugify(
            filename_formatter.FilenameFormatter.format_filename(format_str, sp))
        aac_downloader.concat_chunks(download_path,
                                    downloaded_chunks, filename, 
                                    ffmpeglocation,
                                    withmeta)
        if withmeta is True:
            aac_downloader.add_meta(sp, download_path, filename,
                                    ffmpeglocation)
        m3u8_parser.cleanup(download_path, keepm3u8)
        
    if space_id is not None and guestmode is False:

        print(f"[TSLAZER] ATTEMPTING TO DOWNLOAD SPACE FROM SPACE ID {space_id}")
        sp = get_space.get_space(space_id, authtoken,
                                crsftoken, cookies)
        media_key = parse_utils.get_media_key(sp)
        data = get_urls.get_data(media_key, authtoken, cookies)
        more_data = parse_utils.parse_data(download_path, data, writeinfo)
        get_space.wait_for_end(space_id, sp, authtoken,
                            crsftoken, cookies)
        master_data = parse_utils.parse_master_data(more_data[0])
        cli_prettifier.prettify_metadata(sp)
        cli_prettifier.prettify_urls(more_data[0], master_data[2],
                                    more_data[1], more_data[2], more_data[-1])
        m3u8_file = m3u8_parser.get_m3u8(master_data[2], download_path)
        chunk_urls = m3u8_parser.parse_m3u8(download_path, master_data[0], m3u8_file)
        downloaded_chunks = aac_downloader.download_chunks(download_path, chunk_urls)
        aac_downloader.patch_chunks(download_path, downloaded_chunks)
        filename = soft_slugify.soft_slugify(
            filename_formatter.FilenameFormatter.format_filename(format_str, sp))
        aac_downloader.concat_chunks(download_path,
                                    downloaded_chunks, filename, 
                                    ffmpeglocation,
                                    withmeta)
        if withmeta is True:
            aac_downloader.add_meta(sp, download_path, filename,
                                    ffmpeglocation)
        m3u8_parser.cleanup(download_path, keepm3u8)

    if generatevideo is True and space_id is not None:
        creator_pfp = sp["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["profile_image_url_https"].replace("_normal", "")
        pfp_filename = f"{uuid.uuid4().hex}.jpg"
        aac_downloader.download_file(creator_pfp, pfp_filename, download_path)
        
        video_generator.generate_template(os.path.join(download_path, f"{filename}.m4a"), os.path.join(download_path, pfp_filename), download_path)
        video_generator.generate_video(ffmpeglocation, f"{filename}.m4a", filename, download_path)
        
        #cleanup
        os.remove(os.path.join(download_path, pfp_filename))
        os.remove(os.path.join(download_path, "generated_template.png"))

def show_help():
    try:
        config = config_utils.open_config('config.toml')
    except FileNotFoundError:
        print("[TSLAZER] UNABLE TO LOCATE CONFIG FILE")

    bannerfile = open(config["cliconfig"]["banner"], 'r', encoding='utf-8')
    banner = bannerfile.read()
    bannerfile.close()
    options = open(config["cliconfig"]["optionsbanner"], 'r', encoding='utf-8')
    optionsbanner = options.read()
    options.close()
    print(banner)
    print(optionsbanner)

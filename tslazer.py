import argparse
import os
import tsengine_config as space_dl

parser = argparse.ArgumentParser(description="Download Twitter Spaces at lazer fast speeds!", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--path", "-p", type=str, default=os.getcwd(), help="Path to download the space")

auth_group = parser.add_argument_group("Authentication Options")
auth_group.add_argument("--authtoken", "-a", type=str, help="Your authentication token")
auth_group.add_argument("--crsftoken", "-ct", type=str, help="Your crsf token")
auth_group.add_argument("--cookies", "-ck", type=str, help="Your cookies")
auth_group.add_argument("--guestmode", "-g", action='store_true', help="Don't use Auth, Create A guest token instead (Not Reccomended)")

spaceID_group = parser.add_argument_group("Downloading from a Space ID/URL")
spaceID_group.add_argument("--space_id", "-s", type=str, help="Twitter Space ID or URL")
spaceID_group.add_argument("--user_id", "-ui", type=str, help="input user ID (REQUIRES AUTH")
spaceID_group.add_argument("--username", "-us", type=str, help="input username (REQUIRES AUTH")
spaceID_group.add_argument("--withchat", "-c", action='store_true', default=False, help="Export the Twitter Space's Chat")
spaceID_group.add_argument("--withmeta", "-wm", action='store_true', default=True, help="Write Metadata to the Audio File")
spaceID_group.add_argument("--withshares", "-ws", action='store_true', default=False, help="Download any shared Tweets")
spaceID_group.add_argument("--generatevideo", "-gv", action='store_true', default=False, help="Generate a shareable video")

fileformat_options = """
    %%Ud Host Display Name   %%Dd Day
    %%Un Host Username       %%Dt Time (UTC)
    %%Ui Host User ID        %%Dl Time (Local)
    %%Du Date (Unix)         %%St Space Title
    %%Dy Year                %%Si Space ID
    %%Dm Month               %%Ca Created At
    %%Sa Started At          %%Ua Updated At
    """
spaceID_group.add_argument("--fileformat", "-f", type=str, help=f"File Format Options: {fileformat_options}")

dyn_group = parser.add_argument_group("Downloading from a dynamic or master URL")
dyn_group.add_argument("--dyn_url", "-d", type=str, help="Twitter Space Master URL or Dynamic Playlist URL")
dyn_group.add_argument("--filename", "-fn", type=str, help="Filename for the Twitter Space")

config_group = parser.add_argument_group("Config options")
config_group.add_argument("--config", "-cf", type=str, help="config file to read (Reccomended)")
config_group.add_argument("--ffmpeglocation", "-fl", type=str, default="ffmpeg", help="FFmpeg Location. Defaults to \"ffmpeg\"")
config_group.add_argument("--info", "-i", type=str, help="Don't download anything, just display information about the space")

flag_group = parser.add_argument_group("Various Flags")
flag_group.add_argument("--keepm3u8", "-km", action='store_true', default=False, help="Keep the m3u8 playlist after downloading is complete")
flag_group.add_argument("--writeinfo", "-wi", action='store_true', default=False, help="Write The URLs and other info to a file")

# TESTS
# Download Twitter Space From Master URL (With Config) - Operational
# Download Twitter Space From Space ID (With Config) - Operational
# Download Twitter Space From Username (With Config) - Operational
# DOwnload Twitter Space From User ID (From Config) - Operational
# Download Twitter Space From Space ID Using Guest API (With Config) - Operational!
# Download Twitter Space From Master URL (No Config)
# Download Twitter Space From Space ID (No Config) - OPERATIONAL!
# Download Twitter Space From User ID (No Config)
# Download Twitter Space From Space ID Using Guest API (No Config)

args = parser.parse_args()

if args.help is True:
    space_dl.show_help()
    exit()

if args.dyn_url != None and args.filename == None:
    print("[TSLAZER] Missing Filename Argument!")
        
if (args.user_id or args.username) and args.guestmode:
    print("[TSLAZER] You are trying to perform an action which requires authentication.")

if args.space_id and args.config:
    space_dl.download_from_config(args.config, args.space_id, None, None, None)
    exit()
    
if args.user_id and args.config:
    space_dl.download_from_config(args.config, user_id=args.user_id)
    exit()
    
if args.username and args.config:
    space_dl.download_from_config(args.config, screen_name=args.username)
    exit()
    
if args.dyn_url and args.filename and args.config:
    space_dl.download_from_config(args.config, dynamic_url=args.dyn_url, output_filename=args.filename)
    exit()
    
if args.space_id and not args.config and not args.authtoken:
    space_dl.download_from_cli(space_id=args.space_id, format_str=args.fileformat, withmeta=args.withmeta, keepm3u8=args.keepm3u8,
                               writeinfo=args.writeinfo, generatevideo=args.generatevideo, ffmpeglocation=args.ffmpeglocation, dlpath=args.path)
    exit()

if args.dyn_url and args.filename and not args.config:
    space_dl.download_from_cli(dynamic_url=args.dyn_url, output_filename=args.filename, keepm3u8=args.keepm3u8, writeinfo=args.writeinfo, 
                               ffmpeglocation=args.ffmpeglocation, dlpath=args.path)
    exit()
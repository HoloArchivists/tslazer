# tslazer.py
# author: ef1500
import os
import argparse
import TwitterSpace

parser = argparse.ArgumentParser(description="Download Twitter Spaces at lazer fast speeds!", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--path", "-p", type=str, help="Path to download the space")
parser.add_argument('--cookies', '-c', type=str, help="Path to your cookie.txt file")
spaceID_group = parser.add_argument_group("Downloading from a Space ID/URL")
spaceID_group.add_argument("--space_id", "-s", type=str, help="Twitter Space ID or URL")
spaceID_group.add_argument("--withchat", "-wc", action='store_true', help="Export the Twitter Space's Chat")

fileformat_options = """
    %%Ud	Host Display Name     %%Dy Year
    %%Un	Host Username         %%Dm Month
    %%Ui	Host User ID          %%Dt Time (Utc)
    %%St	Space Title           %%Dl Time (Local)
    %%Si	Space ID
    """
spaceID_group.add_argument("--fileformat", "-f", type=str, help=f"File Format Options: {fileformat_options}")

dyn_group = parser.add_argument_group("Downloading from a dynamic or master URL")
dyn_group.add_argument("--dyn_url", "-d", type=str, help="Twitter Space Master URL or Dynamic Playlist URL")
dyn_group.add_argument("--filename", "-fn", type=str, help="Filename for the Twitter Space")

flag_group = parser.add_argument_group("Various Flags")
flag_group.add_argument("--writeinfo", "-wi", action='store_true', help="Write the Twitter Space information to a file")
flag_group.add_argument("--keepm3u8", "-km", action='store_true', help="Keep the m3u8 playlist after downloading is complete")

args = parser.parse_args()
if args.fileformat == None and args.space_id != None:
    print("Missing Fileformat!")

if args.dyn_url != None and args.filename == None:
    print("Missing Filename Argument!")

if args.withchat == None:
    args.withchat == False

if args.space_id != None and args.fileformat != None:
    if args.path == None:
        args.path = os.getcwd()
    TwitterSpace.TwitterSpace(space_id=args.space_id, dyn_url=args.dyn_url, filenameformat=args.fileformat, path=args.path, withChat=args.withchat, cookiesPath=args.cookies)

if args.dyn_url != None and args.filename != None:
    if args.path == None:
        args.path = os.getcwd()
    TwitterSpace.TwitterSpace(dyn_url=args.dyn_url, filename=args.filename, path=args.path)

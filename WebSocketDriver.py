# Written by ef1500
# Written to accomadate future expansion of this project (and for customization)
# Can Be Run Seperately from the space Downloader itself.

import os
import argparse
import WebSocketHandler

parser = argparse.ArgumentParser(description="Tslazer's Websocket Driver", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--chatToken", "-c", type=str, help="Chat Token")
parser.add_argument("--filename", "-f", type=str, help="Output Filename")
parser.add_argument("--path", "-p", type=str, help="Path to download the Chat")

args = parser.parse_args()
if args.path == None:
    args.path = os.getcwd()
if args.chatToken == None or args.filename == None:
    print("Missing A Required Argument!")
else:
    # self.playlists.chatToken, self.filenameformat, self.path
    WebSocketHandler.SpaceChat(args.chatToken, args.filename, args.path)
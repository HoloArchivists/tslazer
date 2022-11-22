options = """
Authentication Options
--authtoken     auth token
--crsftoken     crsf token
--cookies       cookies
--guestmode     Don't use Auth, Create A guest token instead (Not Reccomended)

Format options
%Ud Host Display Name   %Dd Day
%Un Host Username       %Dt Time (UTC)
%Ui Host User ID        %Dl Time (Local)
%Du Date (Unix)         %St Space Title
%Dy Year                %Si Space ID
%Dm Month               %Ca Created At
%Sa Started At          %Ua Updated At

Optional Arguments
-h, --help            show this help message and exit
--path PATH, -p PATH  Path to download the space

Downloading from a Space ID/URL:
--space_id SPACE_ID, -s SPACE_ID
                        Twitter Space ID or URL
--withchat, -c          Download the chat and server transcription (Not Finished Yet)
--fileformat FILEFORMAT, -f FILEFORMAT
                            The file format string (see Format Options)
--withmeta              Write Metadata to the Audio File
--withshares            Download any shared Tweets (Not Finished Yet)

Downloading from a dynamic or master URL:
--dyn_url DYN_URL, -d DYN_URL
                      Twitter Space Master URL or Dynamic Playlist URL
--filename FILENAME, -fn FILENAME
                         Filename for the Twitter Space

Space Related Arguments
--ffmpeglocation PATH  Path to FFmpeg (Defaults to 'ffmpeg')
--writeinfo            Write The URLs and other info to a file
--keepm3u8             Keep the m3u8 playlist after downloading is complete
--generatevideo        Generate a shareable mp4 (Not finished Yet)

User Related Arugments (Requires Auth)
--username		input username
--user_id		input user ID

Special Arguments
--config CONFIG_FILE
                input config file (Reccomended)
--info [SPACE_ID, MASTER_URL, DYN_URL]
                Don't Download Anything, Only Display Information About the Space (CLI ONLY)

Example Usage:
tslazer --authtoken AUTH --crsftoken CRSF --cookies COOKIES --format %Ud_%Du --space_id 1lDxLLjAmOLxm
"""
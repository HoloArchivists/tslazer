### Tslazer
This is a program to download Twitter Spaces from the command line.

### Features
- Video Generation
    - You can generate a generate a playable video by using the `-gv` or `--generatevideo` argument in conjunction with a space id/user id/screen name
- Config Files
    - You can use a config file to make things easier for yourself, as well as specify authorization tokens
- Completely Customizable
    - Filenames are completly customizable
    - You can enable/disable metadata
    - You can choose to keep the m3u8 files
    - You can choose to write the space information to a file

Also it's **Lazer** fast. It uses threading to ensure you always get the optimal download speed. 
#### Usage

|  Supported URL Sources | Example|
| :------------: | -------------- |
| Space ID/URL | `tslazer --space_id 1ZkJzbdvLgyJv --fileformat %St_%Ud` |
| Master/Dynamic URL| `tslazer --dyn_url DYN_URL --filename space` |
| User ID| `tslazer --config config.toml --user_id 29659253`|
| Screen Name| `tslazer --config config.toml --username amanekanatach`|

- Note: Downloading from a User ID/Screen Name requires Auth

### Config Files

### Requirements
This program requires `ffmpeg` to work. You can install it using `sudo apt install ffmpeg`.

#### Arguments


    >python3 tslazer.py --help
    usage: tslazer.py [-h] [--path PATH] [--authtoken AUTHTOKEN] [--crsftoken CRSFTOKEN] [--cookies COOKIES] [--guestmode] [--space_id SPACE_ID] [--user_id USER_ID]
                      [--username USERNAME] [--withchat] [--withmeta] [--withshares] [--generatevideo] [--fileformat FILEFORMAT] [--dyn_url DYN_URL] [--filename FILENAME]
                      [--config CONFIG] [--ffmpeglocation FFMPEGLOCATION] [--info INFO] [--keepm3u8] [--writeinfo]

    Download Twitter Spaces at lazer fast speeds!

    options:
      -h, --help            show this help message and exit
      --path PATH, -p PATH  Path to download the space

    Authentication Options:
      --authtoken AUTHTOKEN, -a AUTHTOKEN
                            Your authentication token
      --crsftoken CRSFTOKEN, -ct CRSFTOKEN
                            Your crsf token
      --cookies COOKIES, -ck COOKIES
                            Your cookies
      --guestmode, -g       Don't use Auth, Create A guest token instead (Not Reccomended)

    Downloading from a Space ID/URL:
      --space_id SPACE_ID, -s SPACE_ID
                            Twitter Space ID or URL
      --user_id USER_ID, -ui USER_ID
                            input user ID (REQUIRES AUTH
      --username USERNAME, -us USERNAME
                            input username (REQUIRES AUTH
      --withchat, -c        Export the Twitter Space's Chat
      --withmeta, -wm       Write Metadata to the Audio File
      --withshares, -ws     Download any shared Tweets
      --generatevideo, -gv  Generate a shareable video
      --fileformat FILEFORMAT, -f FILEFORMAT
                            File Format Options:
                                %Ud Host Display Name   %Dd Day
                                %Un Host Username       %Dt Time (UTC)
                                %Ui Host User ID        %Dl Time (Local)
                                %Du Date (Unix)         %St Space Title
                                %Dy Year                %Si Space ID
                                %Dm Month               %Ca Created At
                                %Sa Started At          %Ua Updated At


    Downloading from a dynamic or master URL:
      --dyn_url DYN_URL, -d DYN_URL
                            Twitter Space Master URL or Dynamic Playlist URL
      --filename FILENAME, -fn FILENAME
                            Filename for the Twitter Space

    Config options:
      --config CONFIG, -cf CONFIG
                            config file to read (Reccomended)
      --ffmpeglocation FFMPEGLOCATION, -fl FFMPEGLOCATION
                            FFmpeg Location. Defaults to "ffmpeg"
      --info INFO, -i INFO  Don't download anything, just display information about the space

    Various Flags:
      --keepm3u8, -km       Keep the m3u8 playlist after downloading is complete
      --writeinfo, -wi      Write The URLs and other info to a file


|  Argument  |  Description |
| ------------ | ------------ |
| filename | The filename for the space. There is no need  to specify a file extension, as this is done automatically for you |
| dyn_url | Master URL of a Twitter Space. Ends with `dynamic_playlist.m3u8` or `master_playlist.m3u8` |
| space_id | The Url or id of a Twitter Space. |
| username | the @ handle of the user whose Twitter Space you want to capture |
| user_id | The user ID of the user whose Twitter Space you want to capture |

#### Upcoming features
These are features that I will do my best to implement, but I can't offer any guarantees. 

- Discord Integration
- Space Monitoring
- Scheduled Spaces Support
- Monitor Multiple users at a time
- Chat Replay (With Generate Video)
- More Video Templates

### Special Thanks
[@notpeko](https://github.com/notpeko "@notpeko")

[@Ryu1845](https://github.com/Ryu1845 "@Ryu1845") - Inspiration for the project and additional insight

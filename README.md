### Tslazer

This is a program to download Twitter Spaces from the command line.

Also it's **Lazer** fast. It uses threading to ensure you always get the optimal download speed.

## 🚨 Important Update: July 2023 🚨

Due to recent changes in Twitter's API, you must supply cookies using the `-c` option. Twitter seems to have dissolved the usage of guest tokens, meaning that tslazer can no longer download spaces without authorization/credentials.

#### Usage

| Supported URL Sources | Example                                                                       |
| :-------------------: | ----------------------------------------------------------------------------- |
|     Space ID/URL      | `tslazer --space_id 1ZkJzbdvLgyJv --fileformat %St_%Ud`                       |
|  Master/Dynamic URL   | `tslazer --dyn_url DYN_URL --filename space`                                  |
|     With Cookies      | `tslazer --space_id 1ZkJzbdvLgyJv --cookies cookies.txt --fileformat %St_%Ud` |

For more info on a Netscape HTTP Cookie File see [cookie_spec](https://curl.se/rfc/cookie_spec.html)

### Requirements

This program requires `ffmpeg` to work. You can install it using `sudo apt install ffmpeg`.

#### Arguments

    >python3 tslazer.py --help
    usage: tslazer.py [-h] [--path PATH] [--cookies COOKIES] [--space_id SPACE_ID] [--withchat] [--fileformat FILEFORMAT] [--dyn_url DYN_URL] [--filename FILENAME] [--writeinfo] [--keepm3u8]

    Download Twitter Spaces at lazer fast speeds!

    options:
      -h, --help            show this help message and exit
      --path PATH, -p PATH  Path to download the space
      --cookies COOKIES, -c COOKIES
                            Path to your cookie.txt file

    Downloading from a Space ID/URL:
      --space_id SPACE_ID, -s SPACE_ID
                            Twitter Space ID or URL
      --withchat, -wc       Export the Twitter Space's Chat
      --fileformat FILEFORMAT, -f FILEFORMAT
                            File Format Options:
                                %Ud Host Display Name     %Dy Year
                                %Un Host Username         %Dm Month
                                %Ui Host User ID          %Dt Time (Utc)
                                %St Space Title           %Dl Time (Local)
                                %Si Space ID


    Downloading from a dynamic or master URL:
      --dyn_url DYN_URL, -d DYN_URL
                            Twitter Space Master URL or Dynamic Playlist URL
      --filename FILENAME, -fn FILENAME
                            Filename for the Twitter Space

    Various Flags:
      --writeinfo, -wi      Write the Twitter Space information to a file
      --keepm3u8, -km       Keep the m3u8 playlist after downloading is complete

| Argument | Description                                                                                                     |
| -------- | --------------------------------------------------------------------------------------------------------------- |
| filename | The filename for the space. There is no need to specify a file extension, as this is done automatically for you |
| dyn_url  | Master URL of a Twitter Space. Ends with `dynamic_playlist.m3u8` or `master_playlist.m3u8`                      |
| space_id | The Url or id of a Twitter Space.                                                                               |

#### Upcoming features

These are features that I will do my best to implement, but I can't offer any guarantees.

-   Discord Integration
-   Space Monitoring
-   Scheduled Spaces Support
-   Config Files
-   Monitor Multiple users at a time

### Special Thanks

[@notpeko](https://github.com/notpeko "@notpeko")

[@Ryu1845](https://github.com/Ryu1845 "@Ryu1845") - Inspiration for the project and additional insight

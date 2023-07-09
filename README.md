### Tslazer

This is a program to download Twitter Spaces from the command line.

Also it's **Lazer** fast. It uses threading to ensure you always get the optimal download speed.

## 🚨 Important Update: July 2023 🚨

Due to recent changes in Twitter's API, the current version of this tool is no longer functional. Twitter seems to have dissolved the usage of guest tokens, meaning that tslazer can no longer download spaces without authorization/credentials.

## Project Status

As of July 2023, changes to Twitter's API have rendered tslazer's ability to download Twitter Spaces without authorization or credentials is now broken.

### What Happened?

Twitter seems to have dissloved guest API access and/or twitter's v1.1 API. Because of this, the mechanism to retrieve the metadata for Twitter Spaces is now broken. You can read Twitter's official piece on it [here](https://twittercommunity.com/t/reminder-to-migrate-to-the-new-free-basic-or-enterprise-plans-of-the-twitter-api/189737). The API features required to retrieve and download spaces are now locked behind a paywall. However, you may have luck with downloading Twitter Spaces with the [Twitter Space Overhaul](https://github.com/HoloArchivists/tslazer/tree/twitter-space-overhaul) branch, though I'm uncertain.

### How can I help?

If you have a solution to bypass this paywall, restore functionality, or renovate the tool, I **strongly implore** you to lend your invaluable contribution and helping hand. I believe that the only way we as programmers can overcome this is with the power of teamwork. The power to recusitate this project and tool lies in **your** hands.

I have begun a [wiki](https://github.com/HoloArchivists/tslazer/wiki) for this project, where I attempt to explain how the mechanics of Twitter Spaces work, and I would encourage you to start there if you are interested and/or want to contribute.

**Note: If you would like extended functionality, please use the 'twtiter-space-overhaul' branch.**

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
    usage: tslazer.py [-h] [--path PATH] [--space_id SPACE_ID] [--withchat] [--fileformat FILEFORMAT] [--dyn_url DYN_URL] [--filename FILENAME]

    Download Twitter Spaces at lazer fast speeds!

    optional arguments:
      -h, --help            show this help message and exit
      --path PATH, -p PATH  Path to download the space

    Downloading from a Space ID/URL:
      --space_id SPACE_ID, -s SPACE_ID
                            Twitter Space ID or URL
      --cookies -c          Filepath for your cookies.txt file
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

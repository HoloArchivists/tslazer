### Tslazer
This is a program to download Twitter Spaces from the command line. It's also a minimalistic alternative to Ryu1845's twspace-dl.

Also it's **Lazer** fast. It uses threading to ensure you always get the optimal download speed. 
#### Usage

|  Supported URL Sources | Example|
| :------------: | -------------- |
| Space ID/URL | `tslazer --space_id 1ZkJzbdvLgyJv --fileformat %St_%Ud` |
| Master/Dynamic URL| `tslazer --dyn_url DYN_URL --filename space` |

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
      --withchat, -c        Export the Twitter Space's Chat
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


|  Argument  |  Description |
| ------------ | ------------ |
| filename | The filename for the space. There is no need  to specify a file extension, as this is done automatically for you |
| dyn_url | Master URL of a Twitter Space. Ends with `dynamic_playlist.m3u8` or `master_playlist.m3u8` |
| space_id | The Url or id of a Twitter Space. |

#### Upcoming features
These are features that I will do my best to implement, but I can't offer any guarantees. 

- Discord Integration
- Space Monitoring
- Scheduled Spaces Support
- Config Files
- Monitor Multiple users at a time

### Special Thanks
[@notpeko](https://github.com/notpeko "@notpeko")

[@Ryu1845](https://github.com/Ryu1845 "@Ryu1845") - Inspiration for the project and additional insight

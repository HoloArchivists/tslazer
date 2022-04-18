### Tslazer
This is a program to download Twitter Spaces from the command line. 

As of now, this tool cannot download ongoing spaces (Well it can, but the final product will be partial). It works best for ended spaces that you have the master URL for. 
#### Usage

|  Supported URL Sources | Example|
| :------------: | -------------- |
|   Master URL | `tslazer --filename twitter_space --master_url https://master-url` |
| Space URL | `tslazer -space_url https://twitter.com/i/spaces/1ZkJzbdvLgyJv --filename %St_%Un` |
| Space ID | `tslazer --space_id 1ZkJzbdvLgyJv --filename %St_%Ud` |
| Username| `tslazer --auth your_auth_token --username LaplusDarknesss`
| User ID | `tslazer --auth your_auth_token --user_ID 1409817096523968513 --filename %St_%Ud`|

#### Arguments


    >tslazer-rewrite --help
    Allowed Options:
    
    Special Arguments:
      -h [ --help ]          Displays the help page
    
    Required Arguments:
      -a [ --auth ] arg      Your twitter account's auth token
      -f [ --filename ] arg  File Format (see Format options)
                              NOTE: The File Formatting Options are not comaptible
                             with Master URLs.
                             Format options
                             %Ud Host Display Name          %Dd Day
                             %Un Host Username              %Dt Time (UTC)
                             %Ui Host User ID               %Dl Time (Local)
                             %St Space Title                %Si Space ID
                             %Dy Year                       %Dm Month
    
    Link Arguments:
      --master_url arg       Input Master URL
      --space_url arg        Input Space URL
      --space_id arg         Input Space ID
    
    User-Related Arguments:
      --username arg         Input Username
      --user_id arg          Input User ID

|  Argument  |  Description |
| ------------ | ------------ |
|   auth | Your authorization token. Not needed unless you are capturing a Twitter Space from a user ID or a username.  |
|  filename | The filename for the space. There is no need  to specify a file extension, as this is done automatically for you|
| master_url | Master URL of a Twitter Space. Ends with `dynamic_playlist.m3u8` |
| space_url | The Url of a Twitter Space. |
| space_id | The ID of a Twitter Space. This is the 13 character sequence found at the end of the space url.
| username | Capture an ongoing space from the username specified. |
| user_id | Capture ongoing Twitter space from the user_id specified. |

#### File Explanations
| Filename  | Explanation  |
| ------------ | ------------ |
|  TwitterSpaceAPI |  Provides an Interface for the program to interact with Twitter Spaces |
| m3u8_parser  | Provides an interface for the program to Parse the m3u8 files and Download Twitter Spaces  |
| test.cpp  | Provides the Program options and CLI interface  |

#### Upcoming features
These are features that I will do my best to implement, but I can't offer any guarantees. 

- Cross-Platform Support (Hopefully)
- Discord Integration
- Scheduled Spaces Support
- Config Files
- Monitor Multiple users at a time

### Special Thanks
[@notpeko](https://github.com/notpeko "@notpeko") - Writing the code to parse and strip ID3 tags from .aac files.

[@Ryu1845](https://github.com/Ryu1845 "@Ryu1845") - Inspiration for the project and additional insight

### Libraries Used
[CPR Requests Library](https://docs.libcpr.org/ "CPR Requests Library")

[The Boost C++ Libraries](https://www.boost.org/ "The Boost C++ Libraries")

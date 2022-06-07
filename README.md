### Tslazer
This is a program to download Twitter Spaces from the command line. 

Also it's **Lazer** fast. It uses dynamic threading to ensure you always get the optimal download speed. 
#### Usage

|  Supported URL Sources | Example|
| :------------: | -------------- |
| Space ID/URL | `tslazer --space_id 1ZkJzbdvLgyJv --fileformat %St_%Ud` |
| Master/Dynamic URL| `tslazer --dyn_url DYN_URL --filename space` |

#### Arguments


    >python3 tslazer.py --help
    Allowed Options:
    
    Special Arguments:
      -h [ --help ]          Displays the help page
    
    Required Arguments:
      -f [ --fileformat ] arg  File Format (see Format options)
                              NOTE: The File Formatting Options are not comaptible
                             with Master URLs.
                             Format options
                                %Ud	Host Display Name
                                %Un	Host Username
                                %Ui	Host User ID
                                %St	Space Title
                                %Si	Space ID
    
    Link Arguments:
      --dyn_url arg          Input Master/Dynamic URL
      --space_id arg         Input Space ID/URL

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

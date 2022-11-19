def prettify_urls(location, source, status, stream_type, share_url):
    """
    Prettify Twitter Space URLs So we can make them look neat on the screen
    """
    print(f"""[Twitter Space URL Information]
Master URL: {location}
Chunk Playlist: {source}
Stream Status: {status}
Stream Type: {stream_type}
Share URL: {share_url}
""")

def prettify_metadata(metadata):
    """
    Prettify the Twitter Space Metadata so it looks neat on the terminal
    """
    print(f"""[Twitter Space Information]
Title: {metadata["data"]["audioSpace"]["metadata"]["title"]}
Space ID: {metadata["data"]["audioSpace"]["metadata"]["rest_id"]}
Host Display Name: {metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["name"]}
Host Screen Name: {metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["screen_name"]}
Host User ID: {metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["rest_id"]}
""")

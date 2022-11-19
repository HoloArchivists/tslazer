def soft_slugify(filename):
    """Slugify Filenames

    Args:
        filename (str): Filename to Slugify

    Returns:
        str: Slugified Filename
    """
    illegal_chars = ["%", "\\", "/", "<", ">", "*", ":", "\"", "|" ]
    for char in illegal_chars:
        filename = filename.replace(char, "")
    return filename

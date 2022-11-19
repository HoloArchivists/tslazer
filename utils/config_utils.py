import toml

def open_config(config_file):
    """Open .toml file

    Args:
        config_file (str): path to config file or filename

    Returns:
        dict: toml config
    """
    toml_config = toml.load(config_file)
    return toml_config

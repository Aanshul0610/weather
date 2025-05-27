import json 
def load_config():
    """
    Load the configuration from a JSON file.
    
    Returns:
        dict: The configuration dictionary.
    """
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config
def save_config(config):
    """Save the configuration to a JSON file.
    Args:
        config (dict): The configuration dictionary to save.
    """
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
        
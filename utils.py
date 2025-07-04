import json
import os

# Use absolute path for config.json
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

def load_config():
    """
    Load configuration from JSON file. Create a default config if not found.
    """
    if not os.path.exists(CONFIG_FILE):
        print(f"⚠️ {CONFIG_FILE} not found. Creating default configuration...")
        default_config = {
            "api_key": "671e070c61b542ccac890712250106",
            "location": "London",
            "units": "metric"
        }
        save_config(default_config)
        print(f"✅ Default config created. Please update {CONFIG_FILE} with your API key and preferences.")
        return default_config
    else:
        try:
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)
            return config
        except json.JSONDecodeError:
            print(f"❌ {CONFIG_FILE} is not a valid JSON file.")
            return {}

def save_config(config):
    """
    Save the configuration to JSON file.
    """
    try:
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)
        print(f"✅ Configuration saved to {CONFIG_FILE}.")
    except Exception as e:
        print(f"❌ Failed to save config: {e}")
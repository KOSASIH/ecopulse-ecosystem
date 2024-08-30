import json
import os

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_config(self, key):
        return self.config.get(key)

    def set_config(self, key, value):
        self.config[key] = value
        self.save_config()

# Example usage:
if __name__ == "__main__":
    config_manager = ConfigManager()
    config_manager.set_config("api_key", "YOUR_API_KEY")
    print(config_manager.get_config("api_key"))

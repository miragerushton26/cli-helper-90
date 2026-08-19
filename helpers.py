import json

class ConfigLoader:
    def __init__(self, default_config, custom_config_path=None):
        self.default_config = default_config
        self.custom_config = self.load_custom_config(custom_config_path) if custom_config_path else {}

    def load_custom_config(self, path):
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            raise ValueError('Invalid JSON in the configuration file.')

    def get_config(self):
        combined_config = self.default_config.copy()
        combined_config.update(self.custom_config)
        return combined_config

# Example defaults
if __name__ == '__main__':
    defaults = {'host': 'localhost', 'port': 8080, 'debug': False}
    loader = ConfigLoader(defaults, 'config.json')
    config = loader.get_config()
    print(config)
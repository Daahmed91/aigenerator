import json
from groq import Groq

def load_config(config_file='config.json'):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

config = load_config()
client = Groq(api_key=config.get("api_key"))

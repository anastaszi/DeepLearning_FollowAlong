import os
from dotenv import load_dotenv
import json
from pprint import pprint
from pathlib import Path


def load_env_vars(key):
    load_dotenv()
    if key:
        return os.getenv(key)
    return None

def has_json_extension(filepath):
    return Path(filepath).suffix.lower() == '.json'

def print_json(path):
    if os.path.exists(path) and has_json_extension(path):
        with open(path, 'r') as f:
           data = json.load(f)
        
        pprint(data)
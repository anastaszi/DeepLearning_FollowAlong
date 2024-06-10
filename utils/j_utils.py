import os
from dotenv import load_dotenv


def load_env_vars(file_path, key=None):
    load_dotenv(file_path)
    if key:
        return os.getenv(key)
    return None
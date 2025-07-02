import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(key: str, default: str = None) -> str:
    """
    Get an environment variable, return default if not found.
    """
    return os.getenv(key, default)

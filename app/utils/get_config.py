from dotenv import dotenv_values
from pathlib import Path

def get_config():
    root = Path().absolute().parent
    config_env = {
        **dotenv_values(str(root) + "\.env"),
    }
    return config_env

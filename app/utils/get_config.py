from dotenv import dotenv_values
from pathlib import Path

def get_config():
    root = Path().absolute()
    config_env = {
        **dotenv_values(str(root) + "\.env.sample"),
    }
    return config_env

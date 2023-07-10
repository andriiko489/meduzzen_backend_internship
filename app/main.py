from fastapi import FastAPI

from app.utils.get_config import get_config

config_env = get_config()
app = FastAPI()


# print(config_env)
@app.get("/")
def health_check():
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"
            }

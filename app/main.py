import uvicorn
from fastapi import FastAPI

from app.utils.get_config import get_config

config_env = get_config()
app = FastAPI()


@app.get("/")
def health_check():
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"
            }


if __name__ == "__main__":
    uvicorn.run(app, host=config_env["HOST"], port=int(config_env["PORT"]))

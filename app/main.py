from functools import lru_cache
import uvicorn
from fastapi import FastAPI

from app.utils import config

app = FastAPI()

@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/")
def health_check():
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"
            }


if __name__ == "__main__":
    uvicorn.run(app, host=get_settings().host, port=get_settings().port)

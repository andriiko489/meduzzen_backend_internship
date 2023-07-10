from functools import lru_cache
import uvicorn
from fastapi import FastAPI

from app.utils import config

app = FastAPI()
settings = config.Settings()

@app.get("/")
def health_check():
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"
            }


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)

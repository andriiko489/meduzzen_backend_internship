import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sqlalchemy

from pydantic import BaseModel
from utils.config import settings

import redis.asyncio as redis
import asyncio
import nest_asyncio

nest_asyncio.apply()


async def connect_redis():
    await redis.from_url("redis://redis:6379")


loop = asyncio.get_event_loop()
loop.run_until_complete(connect_redis())
# SQLAlchemy specific code, as with any other app

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    settings.database_url
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(NoteIn):
    id: int


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"
            }


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)

import logging.config
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from crud.BaseCRUD import BaseCRUD
from crud.UserCRUD import UserCRUD
from schemas import models, schemas
from schemas.schemas import SignUpUser, UpdateUser
from utils.config import settings

# get root logger
logging.basicConfig(filename="logs.txt", level=logging.DEBUG, filemode="w")
logger = logging.getLogger(__name__)

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
    logger.info("Someone check health")
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"
            }


@app.get("/all/")
async def get_users():
    logger.info("Someone want list of all users")
    r = await UserCRUD().get_users()
    return r

@app.get("/get_user/{id}")
async def get_user(id: int):
    r = await UserCRUD().get_user(id)
    return r

@app.post("/add_user")
async def sign_up_user(user: SignUpUser):
    try:
        r = await UserCRUD().add(user)
        return r
    except Exception as e:
        return e

@app.patch("/update_user")
async def update_user(user: UpdateUser):
    r = await UserCRUD().update(user)
    return r

@app.delete("/delete_user")
async def delete_user(id: int):
    r = await UserCRUD().delete(id)
    return r

if __name__ == "__main__":
    logger.info("Starting...")
    uvicorn.run(app, host=settings.host, port=settings.port)
    logger.info("Started successful")

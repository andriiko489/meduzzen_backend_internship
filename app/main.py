import logging.config
from datetime import timedelta
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from jose import jwt

from crud.UserCRUD import user_crud
from schemas.schemas import SignUpUser, UpdateUser, Token
from services.auth import Auth, VerifyToken
from utils.config import settings

logging.basicConfig(filename="logs.txt", level=logging.DEBUG, filemode="w")
logger = logging.getLogger(__name__)

app = FastAPI()

token_auth_scheme = HTTPBearer()

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
    r = await user_crud.get_users()
    return r


@app.get("/get_user/{id}")
async def get_user(id: int):
    r = await user_crud.get_user(id)
    return r


@app.post("/add_user")
async def sign_up_user(user: SignUpUser):
    try:
        r = await user_crud.add(user)
        return r
    except Exception as e:
        return e


@app.patch("/update_user")
async def update_user(user: UpdateUser):
    r = await user_crud.update(user)
    return r


@app.delete("/delete_user")
async def delete_user(id: int):
    r = await user_crud.delete(id)
    return r


@app.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await Auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = Auth.create_access_token(
        data={"sub": user.username, ".email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/public")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! You don't need to be "
                "authenticated to see this.")
    }
    return result


@app.get("/api/private")
def private(response: Response, token: str = Depends(token_auth_scheme)):  # 👈 updated code
    """A valid access token is required to access this route"""
    if not jwt.get_unverified_header(token.credentials) == {"alg": "RS256", "typ": "JWT"}:
        result = VerifyToken(token.credentials).verify()
        if result.get("status"):
            response.status_code = status.HTTP_400_BAD_REQUEST
    else:
        result = Auth().decode_access_token(token)
    return result[".email"]


if __name__ == "__main__":
    logger.info("Starting...")
    uvicorn.run(app, host=settings.host, port=settings.port)
    logger.info("Started successful")

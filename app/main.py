import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse

from routers import users, home
from schemas import schemas
from utils.logger import logger
from utils.config import settings

from fastapi.security import HTTPBearer

token = HTTPBearer()

app = FastAPI()

app.include_router(users.router)
app.include_router(home.router)


@app.exception_handler(StarletteHTTPException)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(schemas.UserResponse(
        msg=str(exc.detail), status_code=exc.status_code
    ).model_dump_json(indent=2)), status_code=exc.status_code)
    #return schemas.UserResponse(msg=str(exc.detail), status_code=exc.status_code, user=None)


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

if __name__ == "__main__":
    logger.info("Starting...")
    uvicorn.run(app, host=settings.host, port=settings.port)
    logger.info("Started successful")

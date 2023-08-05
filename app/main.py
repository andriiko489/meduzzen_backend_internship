import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, home, company, invitation, admin, quiz, question, answer_option
from utils.logger import logger
from utils.config import settings

from fastapi.security import HTTPBearer

token = HTTPBearer()

app = FastAPI()

app.include_router(users.router)
app.include_router(home.router)
app.include_router(company.router)
app.include_router(invitation.router)
app.include_router(admin.router)
app.include_router(quiz.router)
app.include_router(question.router)
app.include_router(answer_option.router)


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

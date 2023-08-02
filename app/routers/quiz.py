from fastapi import APIRouter, Depends

from crud.QuizCRUD import quiz_crud
from schemas import user_schemas, basic_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"])


@router.get("/all/")
async def get_all(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await quiz_crud.get_all()


@router.post("/add/")
async def add(quiz: basic_schemas.Quiz):
    return await quiz_crud.add(quiz)

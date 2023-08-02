from fastapi import APIRouter, Depends

from crud.QuestionCRUD import question_crud
from schemas import user_schemas, quiz_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/question",
    tags=["question"])


@router.get("/all/")
async def get_all(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await question_crud.get_all()


@router.post("/add/")
async def add(question: quiz_schemas.BasicQuestion):
    return await question_crud.add(question)

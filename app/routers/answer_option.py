from fastapi import APIRouter, Depends

from crud.AnswerOptionCRUD import answer_option_crud
from schemas import user_schemas, quiz_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/answer_option",
    tags=["answer_option"])


@router.get("/all/")
async def get_all(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await answer_option_crud.get_all()


@router.post("/add/")
async def add(answer_option: quiz_schemas.AnswerOption):
    return await answer_option_crud.add(answer_option)

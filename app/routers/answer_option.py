from fastapi import APIRouter, Depends, HTTPException

from crud.AnswerOptionCRUD import answer_option_crud
from crud.QuestionCRUD import question_crud
from crud.QuizCRUD import quiz_crud
from crud.UserCRUD import user_crud
from routers import question
from schemas import user_schemas, quiz_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/answer_option",
    tags=["answer_option"])


async def get_role(question_id: int, user_id: int):
    db_question = await question_crud.get(question_id)
    if db_question is None:
        raise HTTPException(detail="Question not found", status_code=404)
    await question.get_role(quiz_id=db_question.quiz_id, user_id=user_id)


@router.get("/all/")
async def get_all(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await answer_option_crud.get_all()


@router.post("/add/")
async def add(answer_option: quiz_schemas.BasicAnswerOption,
              current_user: user_schemas.User = Depends(Auth.get_current_user)):
    role = await get_role(question_id= answer_option.question_id, user_id=current_user.id)
    return await answer_option_crud.add(answer_option)


@router.patch("/delete")
async def delete(answer_option_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    answer_option = await answer_option_crud.get(answer_option_id)
    if not answer_option:
        HTTPException(detail="Answer option not found", status_code=404)
    role = await get_role(question_id=answer_option.question_id, user_id=current_user.id)
    return await answer_option_crud.delete(id=answer_option.id)

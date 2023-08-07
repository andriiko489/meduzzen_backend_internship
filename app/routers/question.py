from fastapi import APIRouter, Depends, HTTPException

from crud.QuestionCRUD import question_crud
from crud.QuizCRUD import quiz_crud
from routers import quiz
from schemas import user_schemas, quiz_schemas
from services.auth import Auth
from utils.responses import ExceptionResponses

router = APIRouter(
    prefix="/question",
    tags=["question"])


async def get_role(quiz_id: int, user_id: int):
    db_quiz = await quiz_crud.get(quiz_id)
    if db_quiz is None:
        raise HTTPException(detail=ExceptionResponses.QUIZ_NOT_FOUND.value, status_code=404)
    await quiz.get_role(company_id=db_quiz.company_id, user_id=user_id)


@router.get("/all/")
async def get_all(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await question_crud.get_all()


@router.post("/add/")
async def add(question: quiz_schemas.BasicQuestion, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    role = await get_role(quiz_id=question.quiz_id, user_id=current_user.id)
    return await question_crud.add(question)


@router.patch("/delete")
async def delete(question_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    question = await question_crud.get(question_id)
    if not question:
        HTTPException(detail=ExceptionResponses.QUESTION_NOT_FOUND.value, status_code=404)
    role = await get_role(quiz_id=question.quiz_id, user_id=current_user.id)
    return await question_crud.delete(id=question.id)


@router.patch("/update")
async def update(question: quiz_schemas.UpdateQuestion,
                 current_user: user_schemas.User = Depends(Auth.get_current_user)):
    db_question = await question_crud.get(question.id)
    if not db_question:
        HTTPException(detail=ExceptionResponses.QUESTION_NOT_FOUND.value, status_code=404)
    role = await get_role(quiz_id=db_question.quiz_id, user_id=current_user.id)

    question = quiz_schemas.Question(**question.model_dump())
    question.quiz_id = db_question.quiz_id
    return await question_crud.update(question)

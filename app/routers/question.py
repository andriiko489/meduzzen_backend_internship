from fastapi import APIRouter, Depends, HTTPException

from crud.QuestionCRUD import question_crud
from crud.QuizCRUD import quiz_crud
from routers import quiz
from schemas import user_schemas, quiz_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/question",
    tags=["question"])


async def get_role(quiz_id: int, user_id: int):
    db_quiz = await quiz_crud.get(quiz_id)
    if db_quiz is None:
        raise HTTPException(detail="Quiz not found", status_code=404)
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
        HTTPException(detail="Question not found", status_code=404)
    role = await get_role(quiz_id=question.quiz_id, user_id=current_user.id)
    return await question_crud.delete(id=question.id)

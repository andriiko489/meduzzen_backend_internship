

from fastapi import APIRouter, Depends, HTTPException

from crud.AnswerOptionCRUD import answer_option_crud
from crud.QuestionCRUD import question_crud
from crud.QuizCRUD import quiz_crud
from crud.UserCRUD import user_crud
from schemas import user_schemas, quiz_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/answer_option",
    tags=["answer_option"])


@router.get("/all/")
async def get_all(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await answer_option_crud.get_all()


@router.post("/add/")
async def add(answer_option: quiz_schemas.BasicAnswerOption, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    question = await question_crud.get(answer_option.question_id)
    if question is None:
        raise HTTPException(detail="Question not found", status_code=404)
    quiz = await quiz_crud.get(question.quiz_id)
    if quiz is None:
        raise HTTPException(detail="Quiz not found", status_code=404)
    role = await user_crud.get_role(user_id=current_user.id, company_id=quiz.company_id)
    if role is None:
        raise HTTPException(detail="Company not found", status_code=404)
    if role.value < 2:
        raise HTTPException(detail="Only admin and owner can do it", status_code=404)
    return await answer_option_crud.add(answer_option)

from fastapi import APIRouter, Depends, HTTPException

from crud.QuizCRUD import quiz_crud
from crud.UserCRUD import user_crud
from schemas import user_schemas, quiz_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"])


@router.get("/all/")
async def get_all(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await quiz_crud.get_all()


@router.post("/add/")
async def add(quiz: quiz_schemas.BasicQuiz, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    role = await user_crud.get_role(user_id=current_user.id, company_id=quiz.company_id)
    if role is None:
        raise HTTPException(detail="Company not found", status_code=404)
    if role.value < 2:
        raise HTTPException(detail="Only admin and owner can do it", status_code=404)
    return await quiz_crud.add(quiz)

from fastapi import APIRouter, Depends, HTTPException

from crud.ProgressQuizCRUD import progress_quiz_crud
from crud.QuizCRUD import quiz_crud
from schemas import user_schemas, quiz_workflow_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/quiz_workflow",
    tags=["quiz_workflow"]
)


@router.post("/start_quiz/")
async def start_quiz(quiz_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    quiz = await quiz_crud.get(quiz_id)
    if not quiz:
        raise HTTPException(detail="Quiz not found", status_code=404)
    progress_quiz = quiz_workflow_schemas.ProgressQuiz(quiz_id=quiz_id, user_id=current_user.id)
    db_progress_quiz = await progress_quiz_crud.add(progress_quiz)
    if not db_progress_quiz:
        raise HTTPException(detail="Something went wrong", status_code=418)
    return await quiz_crud.get(quiz_id)


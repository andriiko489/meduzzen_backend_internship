from fastapi import APIRouter, Depends

from crud.FinishedQuizCRUD import finished_quiz_crud
from schemas import user_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/analytics",
    tags=["quiz_workflow"]
)

@router.get("/rate")
async def get_rate(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    finished_quizzes = await finished_quiz_crud.get_by_user_id(current_user.id)
    total_num_of_questions = sum(quiz.num_of_questions for quiz in finished_quizzes)
    total_scores = sum(quiz.num_of_correct_answers for quiz in finished_quizzes)
    return total_scores / total_num_of_questions if total_num_of_questions > 0 else 0

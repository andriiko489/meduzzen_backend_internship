import datetime

from fastapi import APIRouter, Depends
from collections import defaultdict

from crud.FinishedQuizCRUD import finished_quiz_crud
from schemas import user_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)


@router.get("/rate")
async def get_rate(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    finished_quizzes = await finished_quiz_crud.get_by_user_id(current_user.id)
    total_num_of_questions = sum(quiz.num_of_questions for quiz in finished_quizzes)
    total_scores = sum(quiz.num_of_correct_answers for quiz in finished_quizzes)
    return total_scores / total_num_of_questions if total_num_of_questions > 0 else 0


@router.get("/get_results_by_quizzes")
async def get_results_by_quizzes(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    finished_quizzes = await finished_quiz_crud.get_by_user_id(user_id=current_user.id)
    grouped_quizzes = defaultdict(list)
    for finished_quiz in finished_quizzes:
        grouped_quizzes[finished_quiz.quiz_id].append(finished_quiz)
    result = dict()
    for quiz_key in grouped_quizzes.keys():
        total_num_of_questions = sum(quiz.num_of_questions for quiz in grouped_quizzes[quiz_key])
        total_scores = sum(quiz.num_of_correct_answers for quiz in grouped_quizzes[quiz_key])
        total_time = sum(quiz.time.total_seconds() for quiz in grouped_quizzes[quiz_key])
        rate = total_scores / total_num_of_questions if total_num_of_questions > 0 else 0
        result[quiz_key] = {"total_num_of_questions": total_num_of_questions,
                            "total_scores": total_scores,
                            "total_time": datetime.timedelta(seconds=total_time),
                            "rate": rate}
    return result

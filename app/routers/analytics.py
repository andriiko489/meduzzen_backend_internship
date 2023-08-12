import datetime

from fastapi import APIRouter, Depends, HTTPException
from collections import defaultdict

from crud.FinishedQuizCRUD import finished_quiz_crud
from crud.UserCRUD import user_crud
from schemas import user_schemas
from services.auth import Auth
from utils.responses import ExceptionResponses

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
async def get_results_grouped_by_quizzes(current_user: user_schemas.User = Depends(Auth.get_current_user)):
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


@router.get("/get_company_members_results")
async def get_company_members_results(company_id: int,
                                      current_user: user_schemas.User = Depends(Auth.get_current_user)):
    role = await user_crud.get_role(user_id=current_user.id, company_id=company_id)
    if role.value < 2:
        raise HTTPException(detail=ExceptionResponses.ONLY_OWNER_ADMIN.value, status_code=403)

    finished_quizzes = await finished_quiz_crud.get_by_company_id(company_id)
    grouped_quizzes = defaultdict(list)
    for finished_quiz in finished_quizzes:
        grouped_quizzes[finished_quiz.user_id].append(finished_quiz)

    result = dict()
    for quiz_key in grouped_quizzes.keys():
        total_num_of_questions = sum(quiz.num_of_questions for quiz in grouped_quizzes[quiz_key])
        total_scores = sum(quiz.num_of_correct_answers for quiz in grouped_quizzes[quiz_key])
        total_time = sum(quiz.time.total_seconds() for quiz in grouped_quizzes[quiz_key])
        last_finished_at = max(quiz.finished_at for quiz in grouped_quizzes[quiz_key] if quiz.finished_at)
        rate = total_scores / total_num_of_questions if total_num_of_questions > 0 else 0

        result[quiz_key] = {"total_num_of_questions": total_num_of_questions,
                            "total_scores": total_scores,
                            "total_time": datetime.timedelta(seconds=total_time),
                            "rate": rate,
                            "last_finished_at": last_finished_at}
    return result


@router.get("/get_member_results")
async def get_member_results(user_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    current_user_role = await user_crud.get_role(user_id=current_user.id, company_id=current_user.company_id)
    if not current_user_role.value or current_user_role.value < 2:
        raise HTTPException(detail=ExceptionResponses.ONLY_OWNER_ADMIN.value, status_code=403)
    user_role = await user_crud.get_role(user_id=user_id, company_id=current_user.company_id)
    if not user_role.value or user_role.value < 1:
        raise HTTPException(detail=ExceptionResponses.NOT_MEMBER.value, status_code=403)
    user = await user_crud.get_user(user_id)
    return await get_results_grouped_by_quizzes(user)

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from crud.AnswerOptionCRUD import answer_option_crud
from crud.AnsweredQuestionCRUD import answered_question_crud
from crud.FinishedQuizCRUD import finished_quiz_crud
from crud.ProgressQuizCRUD import progress_quiz_crud
from crud.QuestionCRUD import question_crud
from crud.QuizCRUD import quiz_crud
from db import redis_db
from schemas import user_schemas, quiz_workflow_schemas, quiz_schemas
from services.auth import Auth
from utils.responses import ExceptionResponses

router = APIRouter(
    prefix="/quiz_workflow",
    tags=["quiz_workflow"]
)


@router.post("/start_quiz/")
async def start_quiz(quiz_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    quiz = await quiz_crud.get(quiz_id)
    if not quiz:
        raise HTTPException(detail=ExceptionResponses.QUIZ_NOT_FOUND.value, status_code=404)
    progress_quiz = quiz_workflow_schemas.ProgressQuiz(quiz_id=quiz_id, user_id=current_user.id)
    questions = await question_crud.get_by_quiz_id(quiz_id=quiz_id)
    if len(questions) < 2:
        raise HTTPException(detail=f"Quiz uncompleted, quiz №{quiz_id} must contain at least 2 questions",
                            status_code=403)
    for question in questions:
        answer_options = await answer_option_crud.get_by_question_id(question.id)
        if len(answer_options) < 2:
            raise HTTPException(
                detail=f"Quiz uncompleted, question №{question.id} must contain at least 2 answer options",
                status_code=403)
        correct_answer = await answer_option_crud.get(question.correct_answer_id)
        if not correct_answer:
            raise HTTPException(
                detail=f"Quiz uncompleted, question №{question.id} have correct_answer, that not exist",
                status_code=403)
    progress_quizzes = await progress_quiz_crud.get_all()
    for progress_quiz in progress_quizzes:
        if progress_quiz.user_id == current_user.id:
            raise HTTPException(detail=f"User arleady have quiz №{progress_quiz.quiz_id} in progress",
                                status_code=403)
    db_progress_quiz = await progress_quiz_crud.add(progress_quiz)
    if not db_progress_quiz:
        raise HTTPException(detail=ExceptionResponses.SOMETHING_WRONG.value, status_code=418)

    return await quiz_crud.get(quiz_id)


@router.post("/answer/")
async def answer(question_id: int, chosen_answer_id: int,
                 current_user: user_schemas.User = Depends(Auth.get_current_user)):
    current_user_id = current_user.id
    question = await question_crud.get(question_id)
    if not question:
        raise HTTPException(detail=ExceptionResponses.QUESTION_NOT_FOUND.value, status_code=404)
    chosen_answer = await answer_option_crud.get(chosen_answer_id)
    if not chosen_answer:
        raise HTTPException(detail=ExceptionResponses.QUIZ_NOT_FOUND.value, status_code=404)

    progress_quiz = await progress_quiz_crud.get_by_user_id(current_user.id)
    if not progress_quiz:
        raise HTTPException(detail=ExceptionResponses.QUIZ_NOT_STARTED.value, status_code=404)
    quiz_id = progress_quiz.quiz_id

    questions = await question_crud.get_by_quiz_id(quiz_id=progress_quiz.quiz_id)
    if question not in questions:
        raise HTTPException(detail=ExceptionResponses.HAVENT_QUESTION.value, status_code=404)
    correct_answer_id = question.correct_answer_id

    answered_options = await answer_option_crud.get_by_question_id(question_id=question_id)
    if not answer not in answered_options:
        raise HTTPException(detail=ExceptionResponses.HAVENT_ANSWER.value, status_code=404)

    if await answered_question_crud.get_by_question_id_and_progress_quiz_id(question_id=question_id,
                                                                            progress_quiz_id=progress_quiz.id):
        raise HTTPException(detail=ExceptionResponses.ALREADY_ANSWERED.value, status_code=409)

    answered_question = quiz_workflow_schemas.BasicAnsweredQuestion(question_id=question_id,
                                                                    answer_id=chosen_answer_id,
                                                                    progress_quiz_id=progress_quiz.id)
    db_answered_question = await answered_question_crud.add(answered_question)
    if not db_answered_question:
        raise HTTPException(detail=ExceptionResponses.CANNOT_SAVE.value, status_code=408)
    quiz = await quiz_crud.get(quiz_id)
    result = quiz_schemas.RedisSchema(user_id=current_user_id,
                                      company_id=quiz.company_id,
                                      quiz_id=quiz_id,
                                      answer_id=chosen_answer_id,
                                      is_correct=correct_answer_id == chosen_answer_id)
    await redis_db.add_result(result)
    return db_answered_question


@router.post("/finish_quiz/")
async def finish_quiz(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    progress_quiz = await progress_quiz_crud.get_by_user_id(current_user.id)
    if not progress_quiz:
        raise HTTPException(detail=ExceptionResponses.QUIZ_NOT_STARTED.value, status_code=404)
    progress_quiz_id = progress_quiz.id
    all_questions = await question_crud.get_by_quiz_id(quiz_id=progress_quiz.quiz_id)
    user_answers = await answered_question_crud.get_by_progress_quiz_id(progress_quiz_id=progress_quiz.id)
    num_of_correct_answers = 0
    for user_answer in user_answers:
        question = await question_crud.get(user_answer.question_id)
        if question.correct_answer_id == user_answer.answer_id:
            num_of_correct_answers += 1
    finished_quiz = quiz_workflow_schemas.BasicFinishedQuiz(num_of_questions=len(all_questions),
                                                            num_of_correct_answers=num_of_correct_answers,
                                                            user_id=current_user.id,
                                                            time=datetime.utcnow() - progress_quiz.started_at)
    for user_answer in user_answers:
        await answered_question_crud.delete(user_answer.id)
    await progress_quiz_crud.delete(progress_quiz_id)
    return await finished_quiz_crud.add(finished_quiz)

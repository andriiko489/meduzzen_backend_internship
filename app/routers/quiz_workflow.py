from fastapi import APIRouter, Depends, HTTPException

from crud.AnswerOptionCRUD import answer_option_crud
from crud.ProgressQuizCRUD import progress_quiz_crud
from crud.QuestionCRUD import question_crud
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
    questions = await question_crud.get_by_quiz_id(quiz_id=quiz_id)
    if len(questions) < 2:
        raise HTTPException(detail=f"Quiz uncompleted, quiz №{quiz_id} must contain at least 2 questions", status_code=403)
    for question in questions:
        answer_options = await answer_option_crud.get_by_question_id(question.id)
        if len(answer_options) < 2:
            raise HTTPException(detail=f"Quiz uncompleted, question №{question.id} must contain at least 2 answer options", status_code=403)
        correct_answer = await answer_option_crud.get(question.correct_answer_id)
        if not correct_answer:
            raise HTTPException(
                detail=f"Quiz uncompleted, question №{question.id} have correct_answer, that not exist",
                status_code=403)
    progress_quizzes = await progress_quiz_crud.get_all()
    for progress_quiz in progress_quizzes:
        if progress_quiz.user_id == current_user.id:
            raise HTTPException(detail=f"User arleady have quiz №{progress_quiz.id} in progress",
                          status_code=403)
    db_progress_quiz = await progress_quiz_crud.add(progress_quiz)
    if not db_progress_quiz:
        raise HTTPException(detail="Something went wrong", status_code=418)

    return await quiz_crud.get(quiz_id)


from fastapi import APIRouter, Request, HTTPException, Depends, Body
from fastapi.templating import Jinja2Templates
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
import json

from app.routers.auth import get_is_authenticated, get_current_user
from models.quiz import Quiz
from models.user import User
from sql_enums.base import RoleEnum


router = APIRouter(
    prefix="/quizzes",
    tags=["Quize", "Тесты"],
)

template = Jinja2Templates(directory="site_data/templates")


def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class QuizBase(BaseModel):
    title: str
    description: str
    timer: int
    quiz_description: dict
    quiz_answers: dict
    deadline: Optional[datetime] = None
    max_attempts: int = 1
    min_pass_percentage: float = 60.0

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


class QuizCreate(QuizBase):
    pass


class QuizResponse(QuizBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


class AnswerSubmit(BaseModel):
    question_id: int
    answer: str
    type: str


class QuizSubmit(BaseModel):
    answers: List[AnswerSubmit]


@router.get("/create")
async def add_quizzes(request: Request):
    return template.TemplateResponse(
        "quizzes/add.html",
        {
            "request": request,
            "is_auth": await get_is_authenticated(request),
        },
    )


@router.post("/create")
async def create_quiz(
    quiz_data: QuizCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != RoleEnum.TEACHER:
        raise HTTPException(status_code=403, detail="Только преподаватели могут создавать тесты")
    
    quiz = await Quiz.create(
        user_id=current_user.id,
        **dict(quiz_data)
    )
    
    return {"status": "success", "quiz_id": quiz.id}


@router.get("/")
async def quizzes(request: Request):
    quizzes: list[Quiz] = await Quiz.get_per_user_id(5)
    return template.TemplateResponse(
        "quizzes/home.html",
        {
            "request": request,
            "quizzes": [QuizResponse.model_validate(quiz).model_dump() for quiz in quizzes],
            "is_auth": await get_is_authenticated(request),
        },
    )


@router.get("/{id}")
async def get_quiz(
    id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    quiz = await Quiz.get(id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Тест не найден")
    
    quiz_data = QuizResponse.model_validate(quiz).model_dump()
    # quiz_json = json.dumps(quiz_data, default=str, ensure_ascii=False)
    
    return template.TemplateResponse(
        "quizzes/solve.html",
        {
            "request": request,
            "quiz": quiz,
            "user": current_user,
            "is_auth": await get_is_authenticated(request),
        }
    )


@router.put("/{id}")
async def update_quiz(
    id: int,
    quiz_data: QuizCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    quiz = await Quiz.get(id=id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Тест не найден")
    
    if quiz.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на редактирование этого теста")
    
    await Quiz.update(id=id, **dict(quiz_data))
    
    return {"status": "success"}


@router.delete("/{id}")
async def delete_quiz(id: int, current_user: User = Depends(get_current_user)):
    quiz = await Quiz.get(id=id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Тест не найден")
    
    if quiz.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление этого теста")
    
    await Quiz.delete(id=id)
    return {"status": "success"}


@router.post("/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: int,
    submit_data: QuizSubmit,
    current_user: User = Depends(get_current_user)
):
    quiz = await Quiz.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Тест не найден")
    
    # Здесь можно добавить проверку времени и попыток
    
    # Сохраняем ответы
    try:
        # TODO: Добавить сохранение ответов в базу данных
        return {"status": "success", "message": "Ответы сохранены"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

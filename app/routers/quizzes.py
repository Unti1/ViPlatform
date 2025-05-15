from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.routers.auth import get_is_authenticated
from models.quiz import Quiz


router = APIRouter(
    prefix="/quizzes",
    tags=["Quize", "Тесты"],
)

template = Jinja2Templates(directory="site_data/templates")


@router.get("/create")
async def add_quizzes(request: Request):  # , user_id:int):
    return template.TemplateResponse(
        "quizzes/add.html",
        {
            "request": request,
            "is_auth": await get_is_authenticated(request),
        },
    )


@router.get("/")
async def quizzes(request: Request):  # , user_id:int):
    quizzes: list[Quiz] = await Quiz.get_per_user_id(5)
    return template.TemplateResponse(
        "quizzes/home.html",
        {
            "request": request,
            "quizzes": quizzes,
            "is_auth": await get_is_authenticated(request),
        },
    )

@router.get("/solve/{id}")
async def solve_quiz(request: Request, id: int):
    quiz: list[Quiz] = await Quiz.get(id=5)
    return template.TemplateResponse(
        "quizzes/solve.html",
        {
            "request": request,
            "quiz": quiz,
            "is_auth": await get_is_authenticated(request),
        },
    )

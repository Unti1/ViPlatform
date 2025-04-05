from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from models.quiz import Quiz


router = APIRouter(
    prefix='/quizzes',
    tags=['Quize'],
    )

template = Jinja2Templates(directory= "site_data/templates")

@router.get('/')
async def quizzes(request: Request, user_id:int):
    quizzes: list[Quiz] = await Quiz.get_per_user_id(user_id)
    return template.TemplateResponse('quizzes/home.html', {'request': request, 'quizzes': quizzes})



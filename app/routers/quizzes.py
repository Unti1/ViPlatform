from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from models.quiz import Quiz


router = APIRouter(
    prefix='/quizzes',
    tags=['Quize'],
    )

template = Jinja2Templates(directory= "site_data/templates")

@router.get('/')
def quizzes(request: Request, user_id:int):
    quizzes = Quiz.get_per_user_id(user_id)
    return template.TemplateResponse('quizzes.html', {'request': request, 'quizzes': quizzes})



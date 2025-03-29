from typing import Annotated
from urllib import request
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemas.user import UserRegistration
from models.user import User


router = APIRouter(
    prefix='/signup',
    tags=['Sign Up'],
    )

template = Jinja2Templates(directory= "site_data/templates")

@router.get('/')
async def get_sign_up_form(request: Request):
    return template.TemplateResponse('signup.html', {'request': request})
    
@router.post('/register')
async def register_user(
    request: Request,
    user_data: Annotated[UserRegistration, Depends()]
    ):

    try:
        user_data: dict = dict(user_data)
        user_data.pop("confirm_password")
        user = await User.create(**user_data)
        return {'message': "Пользователь успешно зарегистрирован", "user_id": user.id}
    except ValueError as e:
        return {"message": str(e)}

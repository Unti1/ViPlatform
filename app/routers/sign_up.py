from urllib import request
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas.user import UserRegistration
from models.user import User


router = APIRouter(
    prefix='/signup',
    tags=['Sign Up'],
    )

template = Jinja2Templates(directory= "site_data/templates")

@router.get('/')
async def get_sign_in_form(request: Request):
    return template.TemplateResponse('signup.html', {'request': request})
    
@router.post('/register')
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
    ):

    user_data = {
        'username': username,
        'email': email,
        'password': password,
        'confirm_password': confirm_password
    }


    try:
        user_registration = UserRegistration(**user_data)
        await User.create(**user_data)
        return {'message': "Пользователь успешно зарегистрирован", "data": user_registration}
    except ValueError as e:
        return {"message": str(e)}

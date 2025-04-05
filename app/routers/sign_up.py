from email import message
import secrets
from typing import Annotated
from urllib import request
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi import security, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasicCredentials
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
    username: str = Form(),
    password: str = Form(),
    email: str = Form()
    ):

    try:
        user = await User.create(username=username, password=password, email=email)
        return {'message': "Пользователь успешно зарегистрирован", "user_id": user.id}
    except ValueError as e:
        return {"message": str(e)}

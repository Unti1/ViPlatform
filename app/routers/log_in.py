from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemas.user import UserRegistration, UserSignIn
from models.user import User

router = APIRouter(
    prefix='/signin',
    tags=['Sign In'],
    )

template = Jinja2Templates(directory= "site_data/templates")

@router.get('/')
async def get_sign_in_form(request: Request):
    return template.TemplateResponse('login.html', {'request': request})

@router.post('/login')
async def register_user(
    request: Request,
    data: Annotated[UserSignIn, Depends()]
    ):
    try:
        # msg =  dict(data)
        status, msg = await User.check(**data)
        return {'message': msg}
    except ValueError as e:
        return {"message": str(e)}
    
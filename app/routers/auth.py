from typing import Annotated
from authx import TokenPayload
from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request,
    HTTPException,
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from schemas.user import UserRegistration, UserSignIn
from settings.config import security, auth_config
from models.user import User
from sql_enums.base import GenderEnum

login_router = APIRouter(
    prefix="/signin",
    tags=["Sign In", "Authorization"],
)

template = Jinja2Templates(directory="site_data/templates")


async def get_is_authenticated(request: Request):
    try:
        token = await security.get_access_token_from_request(request)
        security.verify_token(token, verify_csrf=False)
        return True
    except:
        return False


async def get_current_user(request: Request) -> User:
    token = await security.get_access_token_from_request(request)
    payload = security.verify_token(token, verify_csrf=False)
    user = await User.get(id=int(payload.sub))
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user


@login_router.get("/")
async def get_sign_in_form(request: Request):
    return template.TemplateResponse("auth/login.html", {"request": request})


# POST-метод для авторизации с установкой куки
@login_router.get("/login")
async def log_in_func(request: Request, user_data: Annotated[UserSignIn, Depends()]):
    
    status, msg = await User.check(**dict(user_data))

    if status:
        user = await User.get_by_username(username=user_data.username)
        token = security.create_access_token(uid=str(user.id))
        response = RedirectResponse("/")
        response.set_cookie(auth_config.JWT_ACCESS_COOKIE_NAME, token)
        return response

    return {"request": request, "message": msg}


@login_router.get("/info")
async def get_profile(request: Request):
    token = await security.get_access_token_from_request(request)
    return {"token": token}


@login_router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(f"/")
    response.delete_cookie(auth_config.JWT_ACCESS_COOKIE_NAME)
    return response


reg_router = APIRouter(
    prefix="/signup",
    tags=["Sign Up", "Registration"],
)

template = Jinja2Templates(directory="site_data/templates")


@reg_router.get("/")
async def get_sign_up_form(request: Request):
    return template.TemplateResponse("auth/signup.html", {"request": request, 'genders': GenderEnum})


@reg_router.get("/register")
async def register_user(
    request: Request,
    user_data: Annotated[UserRegistration, Depends()]
):
    try:
        user = await User.create(**dict(user_data))
        token = security.create_access_token(uid=str(user.id))
        response = RedirectResponse('/')
        response.set_cookie(auth_config.JWT_ACCESS_COOKIE_NAME, token)
        return response
    except ValueError as e:
        return {"message": str(e)}

from typing import Annotated
from fastapi import (
    APIRouter,
    Cookie,
    Form,
    Header,
    Request,
    Response,
    Depends,
    HTTPException,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi.templating import Jinja2Templates
from uuid import uuid4
from time import time
import secrets

from models.user import User
from schemas.user import UserSignIn

router = APIRouter(
    prefix="/signin",
    tags=["Sign In"],
)

template = Jinja2Templates(directory="site_data/templates")
security = HTTPBasic()


@router.get("/")
async def get_sign_in_form(request: Request):
    return template.TemplateResponse("login.html", {"request": request})


# Проверка пользователя по имени и паролю
async def get_auth_user_username(
    credentials: HTTPBasicCredentials = Depends(security),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    user = await User.get_by_username(credentials.username)
    if not user:
        raise unauthed_exc

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"), user.password.encode("utf-8")
    ):
        raise unauthed_exc

    return user


# Хранилище сессий (временное, замена на БД или Redis в продакшене)
COOKIES: dict[str, dict[str, any]] = {}
SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:
    return uuid4().hex


def get_session_data(session_id: str = Cookie(alias=SESSION_ID_KEY)):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session",
        )
    return COOKIES[session_id]


@router.get("/login-cookie/")
async def auth_login_set_cookie(
    response: Response,
    user: User = Depends(get_auth_user_username),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "user_id": user.id,  # Сохраняем ID пользователя
        "login_at": int(time()),
    }
    response.set_cookie(SESSION_ID_KEY, session_id)
    return {"result": "ok"}


# Проверка куки и возврат данных сессии
@router.get("/check-cookie")
def auth_check_cookie(user_session_data: dict = Depends(get_session_data)):
    return {"message": f"User ID: {user_session_data['user_id']}", **user_session_data}


# POST-метод для авторизации с установкой куки
@router.post("/login")
async def log_in_func(request: Request, username:str = Form(), password:str = Form()):
    try:
        status, msg = await User.check(username=username, password=password)
        if status:
            user = await User.get_by_username(username)
            session_id = generate_session_id()
            COOKIES[session_id] = {
                "user_id": user.id,  # Сохраняем ID пользователя
                "login_at": int(time()),
            }
            response = template.TemplateResponse(
                "success.html", {"request": request, "message": "Login successful"}
            )
            response.set_cookie(SESSION_ID_KEY, session_id)
            return response
        else:
            return template.TemplateResponse(
                "login.html", {"request": request, "message": msg}
            )
    except ValueError as e:
        return template.TemplateResponse(
            "login.html", {"request": request, "message": str(e)}
        )


async def get_user_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if token := None:  # Поиск токена в БД
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )

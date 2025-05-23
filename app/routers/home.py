from fastapi import APIRouter, Depends, Request
from fastapi.dependencies.models import Dependant
from fastapi.templating import Jinja2Templates
from settings.config import security

from app.routers.auth import get_is_authenticated


router = APIRouter(
    prefix="",
    tags=["Home", "Главная"],
)

template = Jinja2Templates("site_data/templates/")


@router.get("/")
async def home(request: Request):
    print(await get_is_authenticated(request))
    return template.TemplateResponse(
        "home.html",
        {"request": request, "is_auth": await get_is_authenticated(request)},
    )

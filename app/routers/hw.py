from authx import TokenPayload
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from settings.config import security

from app.routers.auth import get_is_authenticated

template = Jinja2Templates(directory="site_data/templates")

router = APIRouter(
    prefix="/hw",
    tags=["Training metrials", "Методички"],
)

@router.get("/")
async def home(request: Request, payload: TokenPayload = Depends(security.access_token_required)):
    print(await get_is_authenticated(request))
    return template.TemplateResponse(
        "manual/home.html",
        {"request": request, "is_auth": await get_is_authenticated(request)},
    )

@router.get("/")
async def home(request: Request, payload: TokenPayload = Depends(security.access_token_required)):
    print(await get_is_authenticated(request))
    return template.TemplateResponse(
        "manual/home.html",
        {"request": request, "is_auth": await get_is_authenticated(request)},
    )
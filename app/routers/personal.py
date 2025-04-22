from authx import TokenPayload
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from models.user import User
from settings.config import settings, security
from sql_enums.base import RoleEnum


router = APIRouter(prefix="/lk", tags=["Personal account", "Личный кабинет"])

template = Jinja2Templates(directory=r"site_data/templates/")


@router.get("/")
async def get_account(
    request: Request, payload: TokenPayload = Depends(security.access_token_required)
):
    user: User = await User.get_per_id(int(payload.sub))
    return template.TemplateResponse(
        r"lk/home.html", {"request": request, "user": user, "is_auth": payload.sub}
    )


template = Jinja2Templates(directory=r"site_data/templates/")


@router.get("/set/role")
async def set_user_role(
    role: RoleEnum, payload: TokenPayload = Depends(security.access_token_required)
):
    await User.update(int(payload.sub), role=RoleEnum)
    return {"msg": "Success"}

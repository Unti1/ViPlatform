from email import message
from typing import Annotated
from authx import TokenPayload
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from models.group import Group
from models.user import User
from schemas.group import GroupSchema
from settings.config import security
from sql_enums.base import RoleEnum

router = APIRouter(
    prefix="/group",
    tags=["Group", "Группы"],
)

template = Jinja2Templates("site_data/templates/")


@router.get("/create")
async def create_group(
    data: Annotated[GroupSchema, Depends()],
    payload: TokenPayload = Depends(security.access_token_required),
):
    user: User = await User.get(payload.sub)
    if user.role == RoleEnum.TEACHER:
        new_row: Group = await Group.add(**dict(data))
        return {"message": "success", "group_id": new_row.id}
    else:
        return {'message': 'failure, you don\'t have some permissions for this action' }
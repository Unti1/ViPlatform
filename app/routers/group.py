from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from models.group import Group
from schemas.group import GroupSchema

router = APIRouter(
    prefix="/group",
    tags=["Group"],
)

template = Jinja2Templates('site_data/templates/')

@router.get('/create')
async def create_group(data: Annotated[GroupSchema, Depends()]):
    print(data)
    new_row: Group = await Group.add(**dict(data))
    return {'message': 'success', 'group_id': new_row.id}
    
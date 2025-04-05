from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="",
    tags=["Home"],
)

template = Jinja2Templates("site_data/templates/")


@router.get("/")
async def home(request: Request):
    return template.TemplateResponse("home.html", {"request": request})

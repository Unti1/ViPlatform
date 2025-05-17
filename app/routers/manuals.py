from fastapi import APIRouter, Request, HTTPException, Depends, Body, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
import os
import shutil

from app.routers.auth import get_is_authenticated, get_current_user
from models.group import Group
from models.manual import Manual
from models.user import User
from sql_enums.base import RoleEnum


router = APIRouter(
    prefix="/manuals",
    tags=["Manuals", "Методические пособия"],
)

template = Jinja2Templates(directory="site_data/templates")


class ManualBase(BaseModel):
    title: str
    description: str
    group_id: int


class ManualCreate(ManualBase):
    pass


class ManualResponse(ManualBase):
    id: int
    filepath: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


@router.get("/")
async def manuals(request: Request, current_user: User = Depends(get_current_user)):
    manuals = await Manual.get_all()
    return template.TemplateResponse(
        "manuals/home.html",
        {
            "is_teacher": current_user.role == RoleEnum.TEACHER,
            "request": request,
            "manuals": manuals,
            "user": current_user,
            "is_auth": await get_is_authenticated(request),
        },
    )


@router.get("/create")
async def add_manual(request: Request, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.TEACHER:
        raise HTTPException(status_code=403, detail="Только преподаватели могут создавать методические пособия")
    
    groups: list[Group] = await Group.get_all()
    return template.TemplateResponse(
        "manuals/add.html",
        {
            "request": request,
            "is_auth": await get_is_authenticated(request),
            "groups": groups,
        },
    )


@router.post("/create")
async def create_manual(
    title: str = Body(...),
    description: str = Body(...),
    group_id: int = Body(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != RoleEnum.TEACHER:
        raise HTTPException(status_code=403, detail="Только преподаватели могут создавать методические пособия")
    
    # Создаем директорию для файлов, если её нет
    upload_dir = "uploads/manuals"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Генерируем уникальное имя файла
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = os.path.join(upload_dir, file_name)
    
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Создаем запись в базе данных
    manual = await Manual.add(
        title=title,
        description=description,
        group_id=group_id,
        filepath=file_path
    )
    
    return {"status": "success", "manual_id": manual.id}


@router.get("/{id}")
async def get_manual(
    id: int,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    manual = await Manual.get(id)
    if not manual:
        raise HTTPException(status_code=404, detail="Методическое пособие не найдено")
    
    return template.TemplateResponse(
        "manuals/view.html",
        {
            "request": request,
            "manual": manual,
            "is_auth": await get_is_authenticated(request),
        }
    )


@router.get("/{id}/download")
async def download_manual(id: int, current_user: User = Depends(get_current_user)):
    manual = await Manual.get(id)
    if not manual:
        raise HTTPException(status_code=404, detail="Методическое пособие не найдено")
    
    if not os.path.exists(manual.filepath):
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    return FileResponse(
        manual.filepath,
        filename=os.path.basename(manual.filepath),
        media_type="application/octet-stream"
    )


@router.delete("/{id}")
async def delete_manual(id: int, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.TEACHER:
        raise HTTPException(status_code=403, detail="Только преподаватели могут удалять методические пособия")
    
    manual = await Manual.get(id)
    if not manual:
        raise HTTPException(status_code=404, detail="Методическое пособие не найдено")
    
    # Удаляем файл
    if os.path.exists(manual.filepath):
        os.remove(manual.filepath)
    
    # Удаляем запись из базы данных
    await Manual.delete(id)
    
    return {"status": "success"} 
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from app.schemas.user import UserRegistration

router = APIRouter(
    prefix='/signin',
    tags=['Sign In'],
    )

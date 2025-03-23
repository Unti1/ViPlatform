from fastapi import APIRouter


router = APIRouter(
    prefix='',
    tags=['Home'],
    )

@router.get('/')
async def home():
    return {'message': 'Welcome to the Home Page'}
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from app.routers.home import router as home_router
from app.routers.quizzes import router as quize_router
from app.routers.log_in import router as sign_in_router
from app.routers.sign_up import router as sign_up_router
from app.routers.dashboard import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(sign_up_router)
app.include_router(sign_in_router)
app.include_router(quize_router)
app.include_router(home_router)
app.include_router(dashboard_router)

if __name__ == '__main__':
    uvicorn.run("website:app", reload=True)
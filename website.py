from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.dashboard import router as dashboard_router
from app.routers.auth import login_router as sign_in_router
from app.routers.auth import reg_router as sign_up_router
from app.routers.personal import router as personal_router
from app.routers.quizzes import router as quize_router
from app.routers.group import router as group_router
from app.routers.home import router as home_router
from app.routers.hw import router as homework_router
from app.routers.manuals import router as train_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(sign_up_router)
app.include_router(sign_in_router)
app.include_router(quize_router)
app.include_router(home_router)
app.include_router(homework_router)
app.include_router(dashboard_router)
app.include_router(group_router)
app.include_router(personal_router)
app.include_router(train_router)

if __name__ == "__main__":
    uvicorn.run("website:app", reload=True)

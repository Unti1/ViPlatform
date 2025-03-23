from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from app.routers.home import router as home_router
from app.routers.quize import router as quize_router
from app.routers.sign_in import router as sign_in_router
from app.routers.sign_up import router as sign_up_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

# template = Jinja2Templates(directory= os.path.join(os.path.dirname(os.path.abspath(__file__)), "site_data", "templates"))
template = Jinja2Templates(directory= "site_data/templates")

app.mount("/site_data", StaticFiles(directory= os.path.join( os.path.dirname(os.path.abspath(__file__)), "site_data","static")))

app.include_router(sign_up_router)
app.include_router(sign_in_router)
app.include_router(quize_router)
app.include_router(home_router)

if __name__ == '__main__':
    uvicorn.run("website:app", reload=True)
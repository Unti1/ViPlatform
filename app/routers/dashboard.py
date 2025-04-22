import json
import traceback
from typing import Annotated

from authx import TokenPayload
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from models.dashboard import Dashboard
from models.group import Group
from schemas.dashboard import DashboardSchema
from settings.logger import fastapi_logger
from app.routers.auth import get_is_authenticated, security

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard", "Инт. доски"],
)

template = Jinja2Templates(directory=r"site_data/templates/")


@router.get("/")
async def main_page(
    request: Request, payload: TokenPayload = Depends(security.access_token_required)
):
    dashboards: list[Dashboard] = await Dashboard.get_all_per_id(int(payload.sub))
    groups: list[Group] = await Group.get_all()

    return template.TemplateResponse(
        "dashboards/home.html",
        {
            "request": request,
            "dashboards": dashboards,
            "groups": groups,
            "is_auth": await get_is_authenticated(request),
        },
    )


@router.get("/create")
async def create_dashboard(
    request: Request,
    data: Annotated[DashboardSchema, Depends()],
    payload: TokenPayload = Depends(security.access_token_required),
):
    dash = await Dashboard.add(**dict(data), user_id=int(payload.sub))
    return RedirectResponse(url=f"/dashboard/{dash.dashboard_id}")


@router.get("/{id}")
async def dashboard(request: Request, id: str):
    dash: Dashboard = await Dashboard.get(dashboard_id=id)
    return template.TemplateResponse(
        "dashboards/index.html",
        {
            "request": request,
            "title": dash.title,
            "is_auth": await get_is_authenticated(request),
        },
    )


connections: dict[str, list] = {}


@router.websocket("/ws/dashboard/{dashboard_id}")
async def websocket_endpoint(
    websocket: WebSocket, dashboard_id: str
):  # Используем int, так как id в модели int
    try:
        await websocket.accept()  # Принимаем соединение
        if dashboard_id not in connections:
            connections[dashboard_id] = []
        connections[dashboard_id].append(websocket)

        # Используем ваш асинхронный метод get
        dashboard = await Dashboard.get(dashboard_id=dashboard_id)
        if not dashboard:
            await websocket.send_text(
                json.dumps({"type": "error", "message": "Dashboard not found"})
            )
            await websocket.close(code=1008)
            return

        fastapi_logger.info(f"Connected to dashboard: {dashboard.title}")
        if dashboard.data:
            await websocket.send_text(json.dumps({"type": "update", **dashboard.data}))

        try:
            while True:
                data = await websocket.receive_text()
                # Используем ваш асинхронный метод update
                await Dashboard.update(dashboard_id, json.loads(data))
                for connection in connections[dashboard_id]:
                    await connection.send_text(
                        json.dumps({"type": "update", **json.loads(data)})
                    )
        except WebSocketDisconnect:
            connections[dashboard_id].remove(websocket)
            fastapi_logger.info(f"Disconnected from dashboard {dashboard_id}")
    except Exception as e:
        fastapi_logger.error(f"WebSocket error: {traceback.format_exc()}")
        await websocket.close(code=1011)  # Internal error
        raise e

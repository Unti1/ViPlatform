import json
import traceback
from typing import Annotated

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from models.dashboard import Dashboard
from schemas.dashboard import DashboardSchema
from settings.logger import fastapi_logger

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

template = Jinja2Templates(directory=r"site_data/templates/")


@router.get("/")
async def home():
    return {"message": "Welcome to the Home Page"}


@router.get("/create")
async def create_dashboard(data: Annotated[DashboardSchema, Depends()]):
    dash = await Dashboard.add(**dict(data))
    return {"message": "Success", "dashboar_id": dash.dashboard_id}


@router.get("/{id}")
async def dashboard(request: Request, id: str):
    dash:Dashboard = await Dashboard.get(dashboard_id = id)
    return template.TemplateResponse(
        "dashboards/index.html", {"request": request, "title": dash.title}
    )


connections: dict[str, list] = {}


# @router.websocket("/ws/dashboard/{dashboard_id}")
# async def websocket_endpoint(websocket: WebSocket, dashboard_id: str):
#     try:
#         await websocket.accept()
#         if dashboard_id not in connections:
#             connections[dashboard_id] = []
#         connections[dashboard_id].append(websocket)

#         dashboard: Dashboard = await Dashboard.get(dashboard_id=dashboard_id)
#         print(dashboard.title)

#         if dashboard:
#             await websocket.send_text(json.dumps({"type": "update", **dashboard.data}))
#         # else:
#         # await websocket.send_text(json.dumps({'type': 'error', 'message': 'Dashboard not found'}))

#         try:
#             while True:
#                 data = await websocket.receive_text()
#                 await Dashboard.update(dashboard.id, json.loads(data))
#                 for connection in connections[dashboard_id]:
#                     await connection.send_text(
#                         json.dumps({"type": "update", **json.loads(data)})
#                     )
#         except WebSocketDisconnect:
#             connection[dashboard_id].remove(websocket)
#     except Exception as e:
#         fastapi_logger.error(traceback.format_exc())
#         raise e

@router.websocket("/ws/dashboard/{dashboard_id}")
async def websocket_endpoint(websocket: WebSocket, dashboard_id: str):  # Используем int, так как id в модели int
    try:
        await websocket.accept()  # Принимаем соединение
        if dashboard_id not in connections:
            connections[dashboard_id] = []
        connections[dashboard_id].append(websocket)

        # Используем ваш асинхронный метод get
        dashboard = await Dashboard.get(dashboard_id=dashboard_id)
        if not dashboard:
            await websocket.send_text(json.dumps({'type': 'error', 'message': 'Dashboard not found'}))
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
                    await connection.send_text(json.dumps({"type": "update", **json.loads(data)}))
        except WebSocketDisconnect:
            connections[dashboard_id].remove(websocket)
            fastapi_logger.info(f"Disconnected from dashboard {dashboard_id}")
    except Exception as e:
        fastapi_logger.error(f"WebSocket error: {traceback.format_exc()}")
        await websocket.close(code=1011)  # Internal error
        raise e
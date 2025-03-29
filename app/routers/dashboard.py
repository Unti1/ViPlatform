import json
from typing import Annotated
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from models.dashboard import Dashboard
from schemas.dashboard import DashboardSchema


router = APIRouter(
    prefix='/dashboard',
    tags=['Dashboard'],
    )

template = Jinja2Templates(directory= r"site_data/templates/")

@router.get('/')
async def home():
    return {'message': 'Welcome to the Home Page'}

@router.get('/create')
async def dashboard(data: Annotated[DashboardSchema, Depends()]):
    dash = await Dashboard.add()
    return {'message': 'Success', 'dashboar_id': dash.id}

@router.get('/{id}')
async def dashboard(request: Request, id: str):
    return template.TemplateResponse('dashboards/index.html', {'request': request, 'title': id})

connections = {}

@router.websocket('/ws/dashboard/{dashboard_id}')
async def websocket_endpoint(websocket: WebSocket, dashboard_id: str):
    await websocket.accept()
    if dashboard_id not in connections:
        connections[dashboard_id] = []
    connections[dashboard_id].append(websocket)

    dashboard: Dashboard = await Dashboard.get(dashboard_id = dashboard_id)
    
    if dashboard:
        await websocket.send_text(json.dumps({'type': 'update', **dashboard.data}))
    # else:
        # await websocket.send_text(json.dumps({'type': 'error', 'message': 'Dashboard not found'}))

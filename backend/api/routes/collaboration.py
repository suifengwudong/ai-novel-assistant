"""
WebSocket collaboration routes
"""
import asyncio
from typing import Dict, List, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["collaboration"])

# project_id -> list of active WebSocket connections
_connections: Dict[str, List[WebSocket]] = {}
_lock = asyncio.Lock()


@router.websocket("/ws/projects/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    await websocket.accept()
    async with _lock:
        if project_id not in _connections:
            _connections[project_id] = []
        _connections[project_id].append(websocket)

    # Notify all participants that a user joined
    await _broadcast(project_id, {"type": "user_joined", "project_id": project_id}, exclude=None)

    try:
        while True:
            data = await websocket.receive_json()
            # Relay message to all other participants
            await _broadcast(project_id, data, exclude=websocket)
    except WebSocketDisconnect:
        async with _lock:
            _connections[project_id].remove(websocket)
        await _broadcast(project_id, {"type": "user_left", "project_id": project_id}, exclude=None)


async def _broadcast(project_id: str, message: dict, exclude: Optional[WebSocket]):
    for ws in list(_connections.get(project_id, [])):
        if ws is exclude:
            continue
        try:
            await ws.send_json(message)
        except Exception:
            pass

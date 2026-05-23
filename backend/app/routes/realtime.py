from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.models.schemas import TrafficPredictionRequest
from app.services.prediction_service import TrafficPredictionService
from app.services.simulation_service import TrafficSimulationEngine
from app.websocket.manager import ConnectionManager
from app.dependencies import get_prediction_service

router = APIRouter(prefix="/api/realtime", tags=["realtime"])
manager = ConnectionManager()


@router.websocket("/ws/traffic")
async def traffic_socket(websocket: WebSocket, predictor: TrafficPredictionService = Depends(get_prediction_service)):
    await manager.connect(websocket)
    simulation_engine = TrafficSimulationEngine(predictor)
    try:
        request_data = await websocket.receive_json()
        request = TrafficPredictionRequest(**request_data)
        async for update in simulation_engine.generate_updates(request):
            await websocket.send_json(update)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as exc:
        await websocket.send_json({"error": str(exc)})
        manager.disconnect(websocket)

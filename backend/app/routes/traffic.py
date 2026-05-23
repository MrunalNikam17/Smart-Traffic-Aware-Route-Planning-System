from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_traffic_service
from app.models.schemas import (
    RouteRequest,
    RouteResponse,
    TrafficPredictionRequest,
    TrafficPredictionResponse,
)
from app.services.traffic_service import TrafficService

router = APIRouter(prefix="", tags=["traffic"])


@router.post("/predict", response_model=TrafficPredictionResponse)
def predict_traffic(
    request: TrafficPredictionRequest,
    traffic_service: TrafficService = Depends(get_traffic_service),
):
    if traffic_service is None:
        raise HTTPException(status_code=500, detail="Traffic service unavailable")
    try:
        prediction, confidence = traffic_service.predict(request)
        return TrafficPredictionResponse(traffic_level=prediction, confidence=confidence)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/route", response_model=RouteResponse)
def optimize_route(
    request: RouteRequest,
    traffic_service: TrafficService = Depends(get_traffic_service),
):
    if traffic_service is None:
        raise HTTPException(status_code=500, detail="Traffic service unavailable")
    try:
        routes = traffic_service.optimize_route(request)
        if not routes:
            raise HTTPException(status_code=404, detail="No route found for the requested nodes")
        return RouteResponse(routes=routes)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

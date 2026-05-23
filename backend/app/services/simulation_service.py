import asyncio
from typing import AsyncGenerator, Dict

from app.models.schemas import RouteRequest
from app.services.prediction_service import TrafficPredictionService
from app.utils.feature_utils import is_rush_hour


class TrafficSimulationEngine:
    """Simulate a live traffic feed for real-time clients."""

    def __init__(self, predictor: TrafficPredictionService):
        self.predictor = predictor

    async def generate_updates(self, request: RouteRequest) -> AsyncGenerator[Dict[str, str], None]:
        while True:
            prediction, confidence = self.predictor.predict(request)
            yield {
                "event": "traffic_update",
                "traffic_level": str(prediction),
                "confidence": f"{confidence:.2f}",
                "rush_hour": str(is_rush_hour(request.day, request.time)),
            }
            await asyncio.sleep(2)

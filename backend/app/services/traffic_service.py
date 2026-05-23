from typing import List

from app.models.schemas import RouteRequest, RouteResult, TrafficPredictionRequest
from app.services.prediction_service import TrafficPredictionService
from app.services.routing_service import RouteOptimizationService


class TrafficService:
    """Orchestrates traffic prediction and routing services."""

    def __init__(self, prediction_service: TrafficPredictionService, routing_service: RouteOptimizationService):
        self.prediction_service = prediction_service
        self.routing_service = routing_service

    def predict(self, request: TrafficPredictionRequest):
        return self.prediction_service.predict(request)

    def optimize_route(self, request: RouteRequest) -> List[RouteResult]:
        return self.routing_service.find_top_routes(request)

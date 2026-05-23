from app.config import settings
from app.services.prediction_service import TrafficPredictionService
from app.services.routing_service import RouteOptimizationService
from app.services.traffic_service import TrafficService
import logging


# Lazy singletons to avoid importing model artifacts at module import time
_prediction_service: TrafficPredictionService | None = None
_routing_service: RouteOptimizationService | None = None
_traffic_service: TrafficService | None = None


def get_prediction_service() -> TrafficPredictionService | None:
    global _prediction_service
    if _prediction_service is None:
        try:
            _prediction_service = TrafficPredictionService(
                model_path=settings.model_path,
                scaler_path=settings.scaler_path,
            )
        except FileNotFoundError:
            logging.warning("Model/scaler not found; prediction service not initialized.")
            _prediction_service = None
    return _prediction_service


def get_routing_service() -> RouteOptimizationService | None:
    global _routing_service
    if _routing_service is None:
        predictor = get_prediction_service()
        if predictor is None:
            return None
        _routing_service = RouteOptimizationService(predictor)
    return _routing_service


def get_traffic_service() -> TrafficService | None:
    global _traffic_service
    if _traffic_service is None:
        prediction_service = get_prediction_service()
        routing_service = get_routing_service()
        if prediction_service is None or routing_service is None:
            return None
        _traffic_service = TrafficService(prediction_service, routing_service)
    return _traffic_service

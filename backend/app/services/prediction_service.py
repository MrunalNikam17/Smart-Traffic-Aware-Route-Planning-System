from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd

from app.ml.model_loader import load_model, load_scaler
from app.models.schemas import TrafficPredictionRequest
from app.utils.feature_utils import encode_features


class TrafficPredictionService:
    """Encapsulate model loading and traffic prediction logic."""

    def __init__(self, model_path: str = None, scaler_path: str = None):
        base_dir = Path(__file__).resolve().parents[2]
        self.model_path = Path(model_path) if model_path else base_dir / "ml" / "Optimized_Traffic_Model.pkl"
        self.scaler_path = Path(scaler_path) if scaler_path else base_dir / "ml" / "Traffic_Scaler.pkl"
        self.model = load_model(self.model_path)
        self.scaler = load_scaler(self.scaler_path)

    def _prepare_input(self, request: TrafficPredictionRequest) -> pd.DataFrame:
        return pd.DataFrame(encode_features(
            day=request.day,
            time_str=request.time,
            vehicles=request.vehicles.dict() if hasattr(request.vehicles, "dict") else request.vehicles,
            weather=request.weather,
            road_type=request.road_type,
            holiday=bool(request.holiday),
        ))

    def predict(self, request: TrafficPredictionRequest) -> Tuple[int, float]:
        df = self._prepare_input(request)
        scaled = self.scaler.transform(df)
        prediction = int(self.model.predict(scaled)[0])
        confidence = float(max(self.model.predict_proba(scaled)[0])) if hasattr(self.model, "predict_proba") else 1.0
        return prediction, confidence

    def predict_batch(self, requests: List[TrafficPredictionRequest]) -> List[Dict[str, Any]]:
        rows = [self._prepare_input(request).iloc[0].to_dict() for request in requests]
        df = pd.DataFrame(rows)
        scaled = self.scaler.transform(df)
        predictions = self.model.predict(scaled)
        probabilities = self.model.predict_proba(scaled) if hasattr(self.model, "predict_proba") else None
        results = []
        for index, prediction in enumerate(predictions):
            confidence = float(max(probabilities[index])) if probabilities is not None else 1.0
            results.append({"traffic_level": int(prediction), "confidence": confidence})
        return results

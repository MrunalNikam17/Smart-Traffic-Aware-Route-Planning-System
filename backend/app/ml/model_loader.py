from pathlib import Path
from typing import Tuple

import joblib
from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler


def load_model(model_path: Path) -> BaseEstimator:
    if not model_path.exists():
        raise FileNotFoundError(f"Traffic model not found at {model_path}")
    return joblib.load(model_path)


def load_scaler(scaler_path: Path) -> StandardScaler:
    if not scaler_path.exists():
        raise FileNotFoundError(f"Scaler file not found at {scaler_path}")
    return joblib.load(scaler_path)

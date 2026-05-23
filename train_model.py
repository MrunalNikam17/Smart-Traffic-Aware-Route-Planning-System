"""
Generate and train traffic prediction model.
Creates synthetic training data and saves model + scaler for the backend.
"""

import random
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


def generate_synthetic_traffic_data(n_samples: int = 5000) -> pd.DataFrame:
    """Generate synthetic traffic data for model training."""
    random.seed(42)
    np.random.seed(42)

    data = {
        "Date": np.random.randint(1, 32, n_samples),
        "Day of the week": np.random.randint(1, 8, n_samples),
        "CarCount": np.random.randint(0, 150, n_samples),
        "BikeCount": np.random.randint(0, 100, n_samples),
        "BusCount": np.random.randint(0, 30, n_samples),
        "TruckCount": np.random.randint(0, 40, n_samples),
        "hour": np.random.randint(0, 24, n_samples),
        "minute": np.random.randint(0, 60, n_samples),
        "AM/PM": np.random.randint(0, 2, n_samples),
        "Weather": np.random.randint(1, 4, n_samples),
        "RoadType": np.random.randint(1, 4, n_samples),
        "Holiday": np.random.randint(0, 2, n_samples),
    }

    df = pd.DataFrame(data)
    df["Total"] = df["CarCount"] + df["BikeCount"] + df["BusCount"] + df["TruckCount"]

    # Reorder columns to match expected order
    df = df[
        [
            "Date",
            "Day of the week",
            "CarCount",
            "BikeCount",
            "BusCount",
            "TruckCount",
            "Total",
            "hour",
            "minute",
            "AM/PM",
            "Weather",
            "RoadType",
            "Holiday",
        ]
    ]

    return df


def generate_traffic_labels(df: pd.DataFrame) -> np.ndarray:
    """Generate realistic traffic level labels (1-4) based on features."""
    traffic_levels = []

    for idx, row in df.iterrows():
        # Base traffic level from vehicle count
        total_vehicles = row["Total"]
        if total_vehicles < 30:
            base_level = 1  # Light
        elif total_vehicles < 80:
            base_level = 2  # Normal
        elif total_vehicles < 130:
            base_level = 3  # Heavy
        else:
            base_level = 4  # Congestion

        # Adjust based on hour (rush hours)
        hour = row["hour"]
        if (7 <= hour <= 10) or (16 <= hour <= 19):
            base_level = min(4, base_level + 1)

        # Adjust based on weather
        weather = row["Weather"]
        if weather == 3:  # Rainy
            base_level = min(4, base_level + 1)
        elif weather == 2:  # Cloudy
            base_level = min(4, base_level)

        # Weekend effect (reduce traffic on weekends)
        day = row["Day of the week"]
        if day in (6, 7):  # Weekend
            base_level = max(1, base_level - 1)

        # Holiday effect
        if row["Holiday"] == 1:
            base_level = max(1, base_level - 1)

        traffic_levels.append(base_level)

    return np.array(traffic_levels)


def train_and_save_model(output_dir: Path) -> None:
    """Generate data, train model, and save artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)

    print("🔄 Generating synthetic traffic data...")
    df = generate_synthetic_traffic_data(n_samples=5000)
    print(f"   ✓ Generated {len(df)} training samples")

    print("🔄 Generating traffic labels...")
    y = generate_traffic_labels(df)
    print(f"   ✓ Traffic level distribution: {np.bincount(y)}")

    print("🔄 Training StandardScaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)

    print("🔄 Training RandomForestClassifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_scaled, y)

    # Evaluate
    train_score = model.score(X_scaled, y)
    print(f"   ✓ Training accuracy: {train_score:.4f}")

    # Save model
    model_path = output_dir / "Optimized_Traffic_Model.pkl"
    scaler_path = output_dir / "Traffic_Scaler.pkl"

    print(f"💾 Saving model to {model_path}")
    joblib.dump(model, model_path)

    print(f"💾 Saving scaler to {scaler_path}")
    joblib.dump(scaler, scaler_path)

    print("\n✅ Model training complete!")
    print(f"   - Model: {model_path}")
    print(f"   - Scaler: {scaler_path}")
    print(f"   - Features: {list(df.columns)}")
    print(f"   - Classes: {sorted(np.unique(y).tolist())}")


if __name__ == "__main__":
    # Save to backend/ml directory
    backend_ml_dir = Path(__file__).resolve().parent / "backend" / "ml"
    train_and_save_model(backend_ml_dir)

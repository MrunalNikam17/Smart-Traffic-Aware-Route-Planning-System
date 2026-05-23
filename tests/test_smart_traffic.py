import pytest
import pandas as pd
from sklearn.preprocessing import StandardScaler

from smart_traffic import SmartRoutePlanner, SmartTrafficPredictor, traffic_cost_weight


class DummyModel:
    def predict(self, X):
        counts = X[:, 2:6].sum(axis=1)
        return [3 if count > 50 else 2 for count in counts]

    def predict_proba(self, X):
        return [[0.1, 0.6, 0.2, 0.1] if count > 50 else [0.1, 0.7, 0.1, 0.1] for count in X[:, 2:6].sum(axis=1)]


@pytest.fixture
def dummy_predictor(tmp_path):
    scaler = StandardScaler()
    df = pd.DataFrame({
        "Date": [0, 0],
        "Day of the week": [1, 2],
        "CarCount": [0, 0],
        "BikeCount": [0, 0],
        "BusCount": [0, 0],
        "TruckCount": [0, 0],
        "Total": [0, 0],
        "hour": [0, 0],
        "minute": [0, 0],
        "AM/PM": [0, 0],
        "Weather": [1, 1],
        "RoadType": [1, 1],
        "Holiday": [0, 0],
    })
    scaler.fit(df)
    model_path = tmp_path / "dummy_model.pkl"
    scaler_path = tmp_path / "dummy_scaler.pkl"
    import joblib
    joblib.dump(DummyModel(), model_path)
    joblib.dump(scaler, scaler_path)
    return SmartTrafficPredictor(model_path, scaler_path)


def test_traffic_cost_weight_basic():
    weight = traffic_cost_weight(3, "Rainy", "CityRoad", True)
    assert weight == pytest.approx(2.5 * 1.4 * 1.1 * 1.2)


def test_predictor_batch_predict(dummy_predictor):
    payload = [
        {
            "Date": 0,
            "Day of the week": 5,
            "CarCount": 20,
            "BikeCount": 10,
            "BusCount": 3,
            "TruckCount": 2,
            "Total": 35,
            "hour": 8,
            "minute": 0,
            "AM/PM": 0,
            "Weather": 1,
            "RoadType": 2,
            "Holiday": 0,
        },
        {
            "Date": 0,
            "Day of the week": 6,
            "CarCount": 30,
            "BikeCount": 15,
            "BusCount": 5,
            "TruckCount": 4,
            "Total": 54,
            "hour": 17,
            "minute": 45,
            "AM/PM": 1,
            "Weather": 2,
            "RoadType": 3,
            "Holiday": 1,
        },
    ]
    predictions = dummy_predictor.predict(payload)
    assert predictions == [2, 3]
    probabilites = dummy_predictor.predict_proba(payload)
    assert len(probabilites) == 2
    assert probabilites[0][1] == pytest.approx(0.7)
    assert probabilites[1][1] == pytest.approx(0.6)


def test_route_cost_with_dynamic_vehicle_counts(dummy_predictor):
    planner = SmartRoutePlanner(dummy_predictor)
    planner.add_road("A", "B", 8, "Highway", {"cars": 10, "bikes": 5, "buses": 2, "trucks": 1})
    cost_default, traffic_default = planner.calculate_cost("A", "B", 5, "08:00", "Sunny", False)
    cost_override, traffic_override = planner.calculate_cost(
        "A", "B", 5, "08:00", "Sunny", False, {"cars": 50, "bikes": 30, "buses": 8, "trucks": 5}
    )
    assert traffic_default == 2
    assert traffic_override == 3
    assert cost_override != cost_default

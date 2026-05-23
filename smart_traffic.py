import csv
import math
import os
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import joblib
import networkx as nx
import pandas as pd

warnings.filterwarnings("ignore")

WeatherMapping = {"Sunny": 1, "Cloudy": 2, "Rainy": 3}
RoadTypeMapping = {"Highway": 1, "CityRoad": 2, "NarrowRoad": 3}
TrafficMapping = {"low": 1, "normal": 2, "high": 3, "heavy": 4}


def parse_time(time_str: str) -> Tuple[int, int, int]:
    """Parse a time string into hour, minute, and AM/PM values."""
    if ":" not in time_str:
        raise ValueError("Time format must be HH:MM or HH:MM:SS")
    parts = [int(part) for part in time_str.split(":")[:2]]
    hour, minute = parts
    am_pm = 1 if hour >= 12 else 0
    return hour % 12, minute, am_pm


def is_rush_hour(day: int, time_str: str) -> bool:
    """Detect rush hour based on day of week and time of day."""
    hour, _, _ = parse_time(time_str)
    local_hour = hour if hour != 0 else 12
    weekday = 1 <= day <= 5
    morning_rush = 7 <= local_hour <= 10
    evening_rush = 16 <= local_hour <= 19
    weekend_peak = day in (6, 7) and 11 <= local_hour <= 14
    return (weekday and (morning_rush or evening_rush)) or weekend_peak


def traffic_cost_weight(
    traffic_level: int,
    weather: str,
    road_type: str,
    holiday: bool,
    rush_hour_bonus: float = 1.0,
) -> float:
    """Return cost multiplier for an edge using traffic, weather, road type and holiday."""
    traffic_weights = {1: 1.0, 2: 1.5, 3: 2.5, 4: 4.0}
    weather_multiplier = {"Sunny": 1.0, "Cloudy": 1.1, "Rainy": 1.4}
    road_type_multiplier = {"Highway": 0.9, "CityRoad": 1.1, "NarrowRoad": 1.3}

    base_factor = traffic_weights.get(traffic_level, 1.0)
    weather_factor = weather_multiplier.get(weather, 1.0)
    road_factor = road_type_multiplier.get(road_type, 1.0)
    holiday_factor = 1.2 if holiday else 1.0

    return round(base_factor * weather_factor * road_factor * holiday_factor * rush_hour_bonus, 4)


def encode_features(
    day: int,
    time_str: str,
    vehicles: Dict[str, int],
    weather: str,
    road_type: str,
    holiday: Union[int, bool],
) -> pd.DataFrame:
    """Create a standardized feature DataFrame for one or many prediction samples."""
    hour, minute, am_pm = parse_time(time_str)
    total = vehicles.get("cars", 0) + vehicles.get("bikes", 0) + vehicles.get("buses", 0) + vehicles.get("trucks", 0)
    data = {
        "Date": [0],
        "Day of the week": [day],
        "CarCount": [vehicles.get("cars", 0)],
        "BikeCount": [vehicles.get("bikes", 0)],
        "BusCount": [vehicles.get("buses", 0)],
        "TruckCount": [vehicles.get("trucks", 0)],
        "Total": [total],
        "hour": [hour],
        "minute": [minute],
        "AM/PM": [am_pm],
        "Weather": [WeatherMapping.get(weather, 1)],
        "RoadType": [RoadTypeMapping.get(road_type, 1)],
        "Holiday": [int(bool(holiday))],
    }
    return pd.DataFrame(data)


class SmartTrafficPredictor:
    """Traffic prediction wrapper for a saved model and scaler."""

    def __init__(self, model_path: Union[str, Path], scaler_path: Union[str, Path]):
        self.model_path = Path(model_path)
        self.scaler_path = Path(scaler_path)
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        if not self.scaler_path.exists():
            raise FileNotFoundError(f"Scaler file not found: {self.scaler_path}")
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)

    def preprocess(self, input_df: pd.DataFrame) -> pd.DataFrame:
        return input_df[[
            "Date", "Day of the week", "CarCount", "BikeCount", "BusCount",
            "TruckCount", "Total", "hour", "minute", "AM/PM", "Weather",
            "RoadType", "Holiday"
        ]]

    def predict(self, input_data: Union[pd.DataFrame, List[Dict[str, Any]], Dict[str, Any]]) -> List[int]:
        """Predict traffic levels for one or multiple samples."""
        if isinstance(input_data, dict):
            input_data = [input_data]
        if isinstance(input_data, list):
            df = pd.DataFrame(input_data)
        elif isinstance(input_data, pd.DataFrame):
            df = input_data.copy()
        else:
            raise ValueError("Input data must be DataFrame, dict, or list of dicts")

        if df.empty:
            return []

        df = self.preprocess(df)
        scaled = self.scaler.transform(df)
        return list(self.model.predict(scaled))

    def predict_proba(self, input_data: Union[pd.DataFrame, List[Dict[str, Any]], Dict[str, Any]]) -> List[List[float]]:
        """Return probability estimates for batch traffic predictions."""
        if isinstance(input_data, dict):
            input_data = [input_data]
        if isinstance(input_data, list):
            df = pd.DataFrame(input_data)
        elif isinstance(input_data, pd.DataFrame):
            df = input_data.copy()
        else:
            raise ValueError("Input data must be DataFrame, dict, or list of dicts")

        if df.empty:
            return []

        df = self.preprocess(df)
        scaled = self.scaler.transform(df)
        if hasattr(self.model, "predict_proba"):
            return [list(probs) for probs in self.model.predict_proba(scaled)]
        raise AttributeError("Loaded model does not support probability estimates")


class SmartRoutePlanner:
    """Route planner using a traffic predictor and dynamic graph costs."""

    def __init__(self, predictor: Optional[SmartTrafficPredictor] = None):
        self.predictor = predictor
        self.graph = nx.Graph()

    def add_city(self, node: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a city node to the road network."""
        self.graph.add_node(node, **(metadata or {}))

    def add_road(
        self,
        a: str,
        b: str,
        distance: float,
        road_type: str,
        vehicles: Optional[Dict[str, int]] = None,
    ) -> None:
        """Add a bidirectional road edge with optional baseline vehicle counts."""
        if a == b:
            raise ValueError("Road endpoints must be different nodes")
        self.add_city(a)
        self.add_city(b)
        self.graph.add_edge(
            a,
            b,
            distance=float(distance),
            road_type=road_type,
            vehicles=vehicles or {"cars": 0, "bikes": 0, "buses": 0, "trucks": 0},
        )

    def set_edge_vehicle_counts(self, a: str, b: str, vehicles: Dict[str, int]) -> None:
        """Update vehicle counts for an existing edge."""
        if not self.graph.has_edge(a, b):
            raise KeyError(f"Edge {a}-{b} does not exist")
        self.graph[a][b]["vehicles"] = vehicles

    def _build_predict_row(
        self,
        day: int,
        time_str: str,
        vehicles: Dict[str, int],
        weather: str,
        road_type: str,
        holiday: bool,
    ) -> pd.DataFrame:
        return encode_features(day, time_str, vehicles, weather, road_type, holiday)

    def calculate_cost(
        self,
        a: str,
        b: str,
        day: int,
        time_str: str,
        weather: str,
        holiday: bool,
        vehicles_override: Optional[Dict[str, int]] = None,
    ) -> Tuple[float, int]:
        """Calculate cost and predicted traffic level for a single edge."""
        if self.predictor is None:
            raise RuntimeError("Predictor is required for cost calculation")
        if not self.graph.has_edge(a, b):
            raise KeyError(f"Edge {a}-{b} does not exist")

        edge = self.graph[a][b]
        vehicles = vehicles_override or edge["vehicles"]
        distance = edge["distance"]
        road_type = edge["road_type"]

        sample = self._build_predict_row(day, time_str, vehicles, weather, road_type, holiday)
        traffic_level = int(self.predictor.predict(sample)[0])
        rush_factor = 1.2 if is_rush_hour(day, time_str) else 1.0
        weight = traffic_cost_weight(traffic_level, weather, road_type, holiday, rush_factor)
        return round(distance * weight, 4), traffic_level

    def _scenario_graph(
        self,
        day: int,
        time_str: str,
        weather: str,
        holiday: bool,
        vehicle_overrides: Optional[Dict[Tuple[str, str], Dict[str, int]]] = None,
        global_vehicle_override: Optional[Dict[str, int]] = None,
    ) -> nx.Graph:
        """Build a temporary weighted graph for a given scenario."""
        G = nx.Graph()
        vehicle_overrides = vehicle_overrides or {}
        for u, v, data in self.graph.edges(data=True):
            override = vehicle_overrides.get((u, v)) or vehicle_overrides.get((v, u)) or global_vehicle_override
            cost, traffic_level = self.calculate_cost(u, v, day, time_str, weather, holiday, override)
            G.add_edge(
                u,
                v,
                cost=cost,
                traffic_level=traffic_level,
                distance=data["distance"],
                road_type=data["road_type"],
            )
        return G

    def find_best_route(
        self,
        start: str,
        goal: str,
        day: int,
        time_str: str,
        weather: str,
        holiday: bool,
        vehicle_overrides: Optional[Dict[Tuple[str, str], Dict[str, int]]] = None,
        global_vehicle_override: Optional[Dict[str, int]] = None,
    ) -> Tuple[List[str], float]:
        """Return the single least-cost route between nodes."""
        if not self.graph.has_node(start) or not self.graph.has_node(goal):
            raise KeyError("Start or goal node not found in the graph")

        G = self._scenario_graph(day, time_str, weather, holiday, vehicle_overrides, global_vehicle_override)
        path = nx.shortest_path(G, source=start, target=goal, weight="cost")
        total_cost = sum(G[u][v]["cost"] for u, v in zip(path[:-1], path[1:]))
        return path, round(total_cost, 4)

    def find_k_best_routes(
        self,
        start: str,
        goal: str,
        day: int,
        time_str: str,
        weather: str,
        holiday: bool,
        k: int = 3,
        vehicle_overrides: Optional[Dict[Tuple[str, str], Dict[str, int]]] = None,
        global_vehicle_override: Optional[Dict[str, int]] = None,
    ) -> List[Dict[str, Any]]:
        """Return the top-k alternative routes sorted by total cost."""
        G = self._scenario_graph(day, time_str, weather, holiday, vehicle_overrides, global_vehicle_override)
        routes: List[Dict[str, Any]] = []
        try:
            paths = nx.shortest_simple_paths(G, source=start, target=goal, weight="cost")
            for index, path in enumerate(paths):
                if index >= k:
                    break
                total_cost = sum(G[u][v]["cost"] for u, v in zip(path[:-1], path[1:]))
                traffic = [G[u][v]["traffic_level"] for u, v in zip(path[:-1], path[1:])]
                routes.append({
                    "path": path,
                    "total_cost": round(total_cost, 4),
                    "traffic_levels": traffic,
                })
        except nx.NetworkXNoPath:
            pass
        return routes

    def export_route_report(
        self,
        filename: str,
        start: str,
        goal: str,
        day: int,
        time_str: str,
        weather: str,
        holiday: bool,
        results: List[Dict[str, Any]],
    ) -> None:
        """Write route outputs to a CSV report file."""
        fieldnames = [
            "created_at",
            "start",
            "goal",
            "day",
            "time",
            "weather",
            "holiday",
            "path",
            "total_cost",
            "traffic_levels",
        ]
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow({
                    "created_at": datetime.utcnow().isoformat(),
                    "start": start,
                    "goal": goal,
                    "day": day,
                    "time": time_str,
                    "weather": weather,
                    "holiday": int(bool(holiday)),
                    "path": "->".join(row["path"]),
                    "total_cost": row["total_cost"],
                    "traffic_levels": ",".join(str(x) for x in row["traffic_levels"]),
                })

    def visualize_route(self, best_path: List[str]) -> None:
        """Visualize the selected route in the network."""
        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 7))
        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(self.graph, pos, with_labels=True, node_color="lightblue", node_size=1600, edge_color="gray", width=2)
        if best_path and len(best_path) > 1:
            nx.draw_networkx_edges(
                self.graph,
                pos,
                edgelist=list(zip(best_path[:-1], best_path[1:])),
                edge_color="green",
                width=4,
                style="dashed",
            )
        labels = {e: f"{data['distance']} km" for e, data in nx.get_edge_attributes(self.graph, "distance").items()}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.title("Smart Traffic Route Network")
        plt.axis("off")
        plt.show()


def build_default_planner(predictor: Optional[SmartTrafficPredictor] = None) -> SmartRoutePlanner:
    """Construct a default sample network with dynamic edges and vehicles."""
    planner = SmartRoutePlanner(predictor=predictor)
    planner.add_road("A", "B", 8, "Highway", {"cars": 40, "bikes": 30, "buses": 8, "trucks": 5})
    planner.add_road("A", "C", 6, "CityRoad", {"cars": 35, "bikes": 25, "buses": 5, "trucks": 4})
    planner.add_road("B", "D", 7, "CityRoad", {"cars": 30, "bikes": 40, "buses": 6, "trucks": 7})
    planner.add_road("C", "D", 3, "NarrowRoad", {"cars": 25, "bikes": 35, "buses": 5, "trucks": 3})
    planner.add_road("B", "C", 5, "Highway", {"cars": 20, "bikes": 20, "buses": 3, "trucks": 2})
    planner.add_road("D", "E", 9, "CityRoad", {"cars": 18, "bikes": 12, "buses": 4, "trucks": 6})
    planner.add_road("C", "F", 4, "Highway", {"cars": 24, "bikes": 15, "buses": 3, "trucks": 7})
    return planner

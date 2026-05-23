from typing import Dict, List, Optional, Tuple, Any

import networkx as nx

from app.models.schemas import RouteRequest, RouteResult, TrafficPredictionRequest
from app.services.prediction_service import TrafficPredictionService
from app.utils.feature_utils import is_rush_hour, traffic_cost_weight


class RouteOptimizationService:
    """Encapsulate route graph logic, cost estimation, and path search."""

    def __init__(self, predictor: TrafficPredictionService):
        self.predictor = predictor
        self.graph = nx.Graph()
        self._build_default_network()

    def _build_default_network(self) -> None:
        self.add_road("A", "B", distance=8.0, road_type="Highway", vehicles={"cars": 40, "bikes": 30, "buses": 8, "trucks": 5})
        self.add_road("A", "C", distance=6.0, road_type="CityRoad", vehicles={"cars": 35, "bikes": 25, "buses": 5, "trucks": 4})
        self.add_road("B", "D", distance=7.0, road_type="CityRoad", vehicles={"cars": 30, "bikes": 40, "buses": 6, "trucks": 7})
        self.add_road("C", "D", distance=3.0, road_type="NarrowRoad", vehicles={"cars": 25, "bikes": 35, "buses": 5, "trucks": 3})
        self.add_road("B", "C", distance=5.0, road_type="Highway", vehicles={"cars": 20, "bikes": 20, "buses": 3, "trucks": 2})
        self.add_road("D", "E", distance=9.0, road_type="CityRoad", vehicles={"cars": 18, "bikes": 12, "buses": 4, "trucks": 6})
        self.add_road("C", "F", distance=4.0, road_type="Highway", vehicles={"cars": 24, "bikes": 15, "buses": 3, "trucks": 7})

    def add_road(self, a: str, b: str, distance: float, road_type: str, vehicles: Optional[Dict[str, int]] = None) -> None:
        self.graph.add_edge(
            a,
            b,
            distance=distance,
            road_type=road_type,
            vehicles=vehicles or {"cars": 0, "bikes": 0, "buses": 0, "trucks": 0},
        )

    def _edge_cost(self, request: RouteRequest, edge: Dict[str, Any], override_vehicles: Optional[Dict[str, int]] = None) -> Tuple[float, int]:
        vehicles = override_vehicles or edge["vehicles"]
        prediction_payload = TrafficPredictionRequest(
            day=request.day,
            time=request.time,
            weather=request.weather,
            holiday=request.holiday,
            road_type=edge["road_type"],
            vehicles=vehicles,
        )
        traffic_level, _ = self.predictor.predict(prediction_payload)
        rush_factor = 1.2 if is_rush_hour(request.day, request.time) else 1.0
        weight = traffic_cost_weight(traffic_level, request.weather, edge["road_type"], bool(request.holiday), rush_factor)
        return edge["distance"] * weight, traffic_level

    def find_top_routes(self, request: RouteRequest, k: int = 3) -> List[RouteResult]:
        graph = nx.Graph()
        for u, v, edge in self.graph.edges(data=True):
            cost, traffic_level = self._edge_cost(request, edge)
            graph.add_edge(u, v, cost=cost, traffic_level=traffic_level)

        try:
            paths = nx.shortest_simple_paths(graph, source=request.start, target=request.goal, weight="cost")
        except nx.NetworkXNoPath:
            return []

        results: List[RouteResult] = []
        for index, path in enumerate(paths):
            if index >= k:
                break
            path_cost = sum(graph[u][v]["cost"] for u, v in zip(path[:-1], path[1:]))
            traffic_levels = [graph[u][v]["traffic_level"] for u, v in zip(path[:-1], path[1:])]
            results.append(RouteResult(path=path, total_cost=round(path_cost, 4), traffic_levels=traffic_levels))
        return results

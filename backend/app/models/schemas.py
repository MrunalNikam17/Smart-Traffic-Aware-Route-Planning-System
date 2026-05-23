from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class VehicleCounts(BaseModel):
    cars: int = Field(0, ge=0)
    bikes: int = Field(0, ge=0)
    buses: int = Field(0, ge=0)
    trucks: int = Field(0, ge=0)


class TrafficPredictionRequest(BaseModel):
    day: int = Field(..., ge=1, le=7)
    time: str = Field(..., description="Time in HH:MM or HH:MM:SS format")
    weather: str = Field(..., pattern="^(Sunny|Cloudy|Rainy)$")
    road_type: str = Field(..., pattern="^(Highway|CityRoad|NarrowRoad)$")
    holiday: int = Field(..., ge=0, le=1)
    vehicles: VehicleCounts


class TrafficPredictionResponse(BaseModel):
    traffic_level: int
    confidence: float


class RouteRequest(BaseModel):
    start: str
    goal: str
    day: int = Field(..., ge=1, le=7)
    time: str = Field(..., description="Time in HH:MM or HH:MM:SS format")
    weather: str = Field(..., pattern="^(Sunny|Cloudy|Rainy)$")
    holiday: int = Field(..., ge=0, le=1)
    vehicles: VehicleCounts
    top_k: Optional[int] = Field(3, ge=1, le=10)


class RouteResult(BaseModel):
    path: List[str]
    total_cost: float
    traffic_levels: List[int]


class RouteResponse(BaseModel):
    routes: List[RouteResult]

from typing import Dict

WeatherMapping = {"Sunny": 1, "Cloudy": 2, "Rainy": 3}
RoadTypeMapping = {"Highway": 1, "CityRoad": 2, "NarrowRoad": 3}


def parse_time(time_str: str):
    parts = [int(part) for part in time_str.split(":")[:2]]
    hour, minute = parts
    am_pm = 1 if hour >= 12 else 0
    return hour % 12, minute, am_pm


def is_rush_hour(day: int, time_str: str) -> bool:
    hour, _, _ = parse_time(time_str)
    local_hour = 12 if hour == 0 else hour
    weekday = 1 <= day <= 5
    morning_rush = 7 <= local_hour <= 10
    evening_rush = 16 <= local_hour <= 19
    weekend_peak = day in (6, 7) and 11 <= local_hour <= 14
    return (weekday and (morning_rush or evening_rush)) or weekend_peak


def traffic_cost_weight(traffic_level: int, weather: str, road_type: str, holiday: bool, rush_hour_bonus: float = 1.0) -> float:
    traffic_weights = {1: 1.0, 2: 1.5, 3: 2.5, 4: 4.0}
    weather_multiplier = {"Sunny": 1.0, "Cloudy": 1.1, "Rainy": 1.4}
    road_type_multiplier = {"Highway": 0.9, "CityRoad": 1.1, "NarrowRoad": 1.3}
    base_factor = traffic_weights.get(traffic_level, 1.0)
    weather_factor = weather_multiplier.get(weather, 1.0)
    road_factor = road_type_multiplier.get(road_type, 1.0)
    holiday_factor = 1.2 if holiday else 1.0
    return round(base_factor * weather_factor * road_factor * holiday_factor * rush_hour_bonus, 4)


def encode_features(day: int, time_str: str, vehicles: Dict[str, int], weather: str, road_type: str, holiday: bool):
    hour, minute, am_pm = parse_time(time_str)
    total = vehicles.get("cars", 0) + vehicles.get("bikes", 0) + vehicles.get("buses", 0) + vehicles.get("trucks", 0)
    return {
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
        "Holiday": [int(holiday)],
    }

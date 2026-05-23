import argparse
import os
from typing import Dict, Tuple

from smart_traffic import SmartRoutePlanner, SmartTrafficPredictor, build_default_planner


def parse_vehicle_counts(args: argparse.Namespace) -> Dict[str, int]:
    return {
        "cars": args.cars,
        "bikes": args.bikes,
        "buses": args.buses,
        "trucks": args.trucks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Smart Traffic Prediction and Route Optimization CLI")
    parser.add_argument("--model", default="Optimized_Traffic_Model.pkl", help="Path to trained traffic model")
    parser.add_argument("--scaler", default="Traffic_Scaler.pkl", help="Path to trained scaler")
    parser.add_argument("--start", required=True, help="Starting city node")
    parser.add_argument("--goal", required=True, help="Destination city node")
    parser.add_argument("--day", type=int, required=True, help="Day of week as integer 1-7")
    parser.add_argument("--time", required=True, help="Time in HH:MM or HH:MM:SS")
    parser.add_argument("--weather", choices=["Sunny", "Cloudy", "Rainy"], required=True, help="Weather condition")
    parser.add_argument("--holiday", type=int, choices=[0, 1], default=0, help="Holiday flag: 0 or 1")
    parser.add_argument("--cars", type=int, default=0, help="Real-time car count for requested route")
    parser.add_argument("--bikes", type=int, default=0, help="Real-time bike count for requested route")
    parser.add_argument("--buses", type=int, default=0, help="Real-time bus count for requested route")
    parser.add_argument("--trucks", type=int, default=0, help="Real-time truck count for requested route")
    parser.add_argument("--top-k", type=int, default=3, help="Number of alternative routes to return")
    parser.add_argument("--export", default="route_report.csv", help="CSV filename for route export")
    args = parser.parse_args()

    if not os.path.exists(args.model) or not os.path.exists(args.scaler):
        raise FileNotFoundError(
            f"Model or scaler not found. Make sure '{args.model}' and '{args.scaler}' exist in the working directory."
        )

    predictor = SmartTrafficPredictor(args.model, args.scaler)
    planner = build_default_planner(predictor)

    vehicle_override = parse_vehicle_counts(args)
    routes = planner.find_k_best_routes(
        args.start,
        args.goal,
        args.day,
        args.time,
        args.weather,
        bool(args.holiday),
        k=args.top_k,
        global_vehicle_override=vehicle_override,
    )

    if not routes:
        print("No routes were found for the requested nodes and scenario.")
        return

    print("\nTop route options:")
    for index, route in enumerate(routes, start=1):
        print(f"{index}. Path: {' -> '.join(route['path'])}")
        print(f"   Total cost: {route['total_cost']:.4f}")
        print(f"   Edge traffic levels: {route['traffic_levels']}\n")

    planner.export_route_report(
        args.export,
        args.start,
        args.goal,
        args.day,
        args.time,
        args.weather,
        bool(args.holiday),
        routes,
    )
    print(f"Route report exported to {args.export}")


if __name__ == "__main__":
    main()

<div align="center">

# 🚦 Smart Traffic-Aware Route Planning System

**AI-powered route optimization that thinks beyond shortest distance**


> *Traditional GPS finds the shortest path. This system finds the **smartest** one.*

</div>

---

## 🧠 What Makes This Different?

Most routing algorithms minimize **distance**. Real-world navigation demands more — a 10 km highway free of traffic beats a 6 km city road gridlocked in rain during rush hour every time.

This system combines **Machine Learning traffic prediction** with **dynamic graph cost computation** to find the route with the lowest *real-world travel cost*, factoring in:

| Factor | Impact |
|---|---|
| 🚗 Vehicle density (cars, bikes, buses, trucks) | Direct traffic level prediction |
| 🌦️ Weather (Sunny / Cloudy / Rainy) | Up to 1.4× cost multiplier |
| 🛣️ Road type (Highway / City Road / Narrow Road) | 0.9× – 1.3× cost multiplier |
| 📅 Holiday indicator | 1.2× cost multiplier |
| ⏰ Rush hour detection | 1.2× rush bonus |

---

## 📸 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  SMART TRAFFIC SYSTEM                        │
│                                                             │
│  TrafficData.csv ──► Preprocessing ──► Random Forest Train  │
│                                               │              │
│  Real-Time Inputs ──► Feature Encoding ──► Prediction       │
│   (vehicles, weather,        │                │              │
│    time, road type)          │          Traffic Level        │
│                              │          (1=Low → 4=Heavy)   │
│                              ▼                │              │
│              Heuristic Cost Calculation ◄─────┘              │
│          cost = dist × traffic × weather × road × holiday   │
│                              │                               │
│                              ▼                               │
│           Modified Dijkstra / A* on Dynamic Graph           │
│                              │                               │
│                              ▼                               │
│          ✅ Optimal Route  +  📊 Visualization               │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

- **🤖 ML-Powered Traffic Prediction** — Random Forest Classifier with GridSearchCV hyperparameter tuning predicts traffic levels (Low / Normal / High / Heavy) per road segment
- **⚖️ Dynamic Edge Weights** — Every road edge is re-weighted at query time using real-world multipliers, not static estimates
- **🗺️ Top-K Route Alternatives** — Get not just the best route but the top-K alternatives ranked by cost
- **⏰ Rush Hour Intelligence** — Automatically detects morning/evening rush (weekdays) and weekend peak hours
- **📤 CSV Route Reports** — Export detailed route reports for analysis and logging
- **📊 Route Visualization** — Matplotlib network graph with optimal path highlighted in green
- **🖥️ CLI Interface** — Run queries directly from the terminal without writing code
- **🧪 Multi-Scenario Testing** — Evaluate routes across morning rush, midday, rainy holiday evening, and late night

---

## 🏗️ Project Structure

```
Smart-Traffic-Aware-Route-Planning-System/
│
├── 📓 Traffic_pred_best_route.ipynb  # Full end-to-end notebook
├── 🐍 smart_traffic.py               # Core engine (predictor + planner)
├── 🏋️ train_model.py                 # Model training & serialization
├── 💻 cli.py                         # Command-line interface
├── 📊 TrafficData.csv                # Training dataset
│
├── backend/                          # Backend service
├── frontend/                         # Frontend interface
├── tests/                            # Test suites
└── .gitignore
```

---

## 🤖 Machine Learning Model

| Property | Detail |
|---|---|
| **Algorithm** | Random Forest Classifier |
| **Tuning** | GridSearchCV |
| **Target** | Traffic Situation (1–4) |
| **Serialization** | joblib (model + scaler) |

### Input Features

```python
features = [
    "Day of the week",   # 1 (Mon) – 7 (Sun)
    "CarCount",          # Number of cars
    "BikeCount",         # Number of bikes
    "BusCount",          # Number of buses
    "TruckCount",        # Number of trucks
    "Total",             # Sum of all vehicles
    "hour", "minute",    # Time of day
    "AM/PM",             # 0 = AM, 1 = PM
    "Weather",           # 1=Sunny, 2=Cloudy, 3=Rainy
    "RoadType",          # 1=Highway, 2=CityRoad, 3=NarrowRoad
    "Holiday"            # 0 or 1
]
```

### Traffic Level Classes

```
1 → 🟢 Low      (free flow)
2 → 🟡 Normal   (moderate)
3 → 🟠 High     (congested)
4 → 🔴 Heavy    (gridlock)
```

---

## 🧮 Heuristic Cost Function

```
Total Cost = Distance × Traffic Factor × Weather Factor × Road Type Factor × Holiday Factor × Rush Hour Bonus
```

| Component | Values |
|---|---|
| Traffic Factor | 1.0 / 1.5 / 2.5 / 4.0 (Low → Heavy) |
| Weather Factor | Sunny=1.0, Cloudy=1.1, Rainy=1.4 |
| Road Type Factor | Highway=0.9, CityRoad=1.1, NarrowRoad=1.3 |
| Holiday Factor | 1.2 if holiday else 1.0 |
| Rush Hour Bonus | 1.2 during rush hours |

> **Example:** A 5 km Highway segment during Heavy traffic, Rainy weather, on a Holiday:  
> `5 × 4.0 × 1.4 × 0.9 × 1.2 = 30.24 cost units`

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/MrunalNikam17/Smart-Traffic-Aware-Route-Planning-System.git
cd Smart-Traffic-Aware-Route-Planning-System
```

### 2. Install Dependencies

```bash
pip install pandas scikit-learn networkx matplotlib joblib
```

### 3. Train the Model

```bash
python train_model.py
```

### 4. Run via CLI

```bash
python cli.py --start A --goal E --day 2 --time 08:30 --weather Rainy --holiday 0
```

### 5. Or Use the Python API

```python
from smart_traffic import SmartTrafficPredictor, SmartRoutePlanner, build_default_planner

predictor = SmartTrafficPredictor("model.pkl", "scaler.pkl")
planner = build_default_planner(predictor)

# Find the best route
path, cost = planner.find_best_route(
    start="A", goal="E",
    day=2,            # Tuesday
    time_str="08:30",
    weather="Rainy",
    holiday=False
)

print(f"Best Route: {' → '.join(path)}")
print(f"Total Cost: {cost}")

# Visualize
planner.visualize_route(path)
```

### 6. Get Top-K Alternative Routes

```python
routes = planner.find_k_best_routes(
    start="A", goal="E",
    day=2, time_str="08:30",
    weather="Rainy", holiday=False,
    k=3
)

for i, route in enumerate(routes, 1):
    print(f"Route {i}: {' → '.join(route['path'])} | Cost: {route['total_cost']}")
```

---

## 🧪 Test Scenarios

The system is evaluated across diverse real-world conditions:

| Scenario | Day | Time | Weather | Holiday | Expected Behavior |
|---|---|---|---|---|---|
| 🌅 Morning Rush | Weekday | 08:00 | Sunny | No | Highways preferred |
| ☀️ Midday Normal | Weekday | 13:00 | Cloudy | No | Balanced routing |
| 🌧️ Rainy Holiday | Any | 18:00 | Rainy | Yes | High-cost avoidance |
| 🌙 Late Night | Weekday | 23:00 | Sunny | No | Shortest path wins |

---

## 📊 Visualization Output

The route graph displays:
- 🔵 **Blue nodes** — intersections / cities
- ⚫ **Gray edges** — all available roads with distance labels
- 🟢 **Dashed green edges** — the selected optimal route

---

## 🛠️ Core Classes

### `SmartTrafficPredictor`
Wraps the trained Random Forest model and StandardScaler for inference.
```python
predictor = SmartTrafficPredictor("model.pkl", "scaler.pkl")
levels = predictor.predict(feature_df)          # → [1, 3, 2, ...]
probs  = predictor.predict_proba(feature_df)    # → [[0.8, 0.1, ...], ...]
```

### `SmartRoutePlanner`
Manages the road network graph and executes cost-aware routing.
```python
planner = SmartRoutePlanner(predictor)
planner.add_road("A", "B", distance=8, road_type="Highway", vehicles={...})
path, cost = planner.find_best_route(...)
planner.export_route_report("report.csv", ...)
planner.visualize_route(path)
```

---

## 🔮 Future Enhancements

- [ ] Real-time traffic data integration (Google Maps API / HERE API)
- [ ] Live weather feed via OpenWeatherMap
- [ ] Web-based interactive map (Leaflet.js / Folium)
- [ ] Time-expanded graph for departure-time optimization
- [ ] Deep Learning model (LSTM) for sequential traffic prediction
- [ ] REST API backend with FastAPI
- [ ] Docker containerization for easy deployment

---


---

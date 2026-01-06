# 🚦 Smart Traffic-Aware Route Planning System

An **AI-powered smart route planning system** that predicts traffic congestion using **Machine Learning** and computes the **optimal route** using dynamic cost-based graph traversal.

---

## 📌 Overview

Urban traffic conditions change dynamically due to multiple real-world factors such as:

- Vehicle density  
- Weather conditions  
- Road type  
- Time of day  
- Holidays  

Traditional shortest-path algorithms fail to capture these variations.

This project addresses the problem by:

- Predicting traffic levels using a **Random Forest ML model**
- Dynamically adjusting road costs using **heuristic functions**
- Finding the **least-cost route** instead of the shortest-distance route
- Visualizing the optimized route on a **road network graph**

---

## ✨ Key Features

- 🚗 Traffic level prediction using Machine Learning  
- 🗺️ Graph-based road network modeling  
- ⚖️ Dynamic edge cost calculation  
- 🌦️ Weather, road type, and holiday impact modeling  
- 📊 Visual route simulation  
- 🔁 Multi-scenario route evaluation  

---

## 🏗️ System Workflow

Traffic Dataset
↓
Data Preprocessing
↓
Random Forest Model Training
↓
Traffic Level Prediction
↓
Heuristic Cost Calculation
↓
Modified Dijkstra / A* Algorithm
↓
Optimal Route Visualization
---


---

## ⚙️ Technologies Used

- Python  
- Pandas  
- Scikit-learn  
- NetworkX  
- Matplotlib  
- Joblib  

---

## 🤖 Machine Learning Model

- **Algorithm:** Random Forest Classifier  
- **Hyperparameter Tuning:** GridSearchCV  
- **Target Variable:** Traffic Situation  

### Traffic Levels

- **1** → Low  
- **2** → Normal  
- **3** → High  
- **4** → Heavy  

### Input Features

- Vehicle counts (cars, bikes, buses, trucks)  
- Total vehicle count  
- Time (hour, minute, AM/PM)  
- Day of the week  
- Weather condition  
- Road type  
- Holiday indicator  

---

## 🧮 Heuristic Cost Function

Each road’s cost is dynamically calculated as:

Total Cost =
Distance × Traffic Factor × Weather Factor × Road Type Factor × Holiday Factor
This ensures:

- Congested roads are penalized  
- Rainy and narrow roads increase cost  
- Highways are preferred during low traffic  

---

## 🛣️ Routing Algorithm

- Modified **Dijkstra / A\*** algorithm  
- Priority queue–based traversal  
- Cycle avoidance  
- Dynamic edge weights updated using ML predictions  

The algorithm selects the **least-cost route**, not just the shortest path.

---

## 📊 Visualization

- Nodes represent intersections  
- Edges represent roads  
- Optimal route highlighted using **dashed green edges**  
- Distance labels displayed on each road  

---

## 🧪 Test Scenarios

Routes are evaluated under multiple conditions:

- Morning rush hours  
- Midday traffic  
- Rainy holiday evenings  
- Late-night low traffic  

Each scenario dynamically changes:

- Traffic predictions  
- Road costs  
- Selected optimal route  

---



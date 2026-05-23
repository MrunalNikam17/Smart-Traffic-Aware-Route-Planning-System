import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface VehicleCounts {
  cars: number
  bikes: number
  buses: number
  trucks: number
}

export interface TrafficPredictionRequest {
  day: number
  time: string
  weather: 'Sunny' | 'Cloudy' | 'Rainy'
  road_type: 'Highway' | 'CityRoad' | 'NarrowRoad'
  holiday: number
  vehicles: VehicleCounts
}

export interface TrafficPredictionResponse {
  traffic_level: number
  confidence: number
}

export interface RouteResult {
  path: string[]
  total_cost: number
  traffic_levels: number[]
}

export interface RouteRequest {
  start: string
  goal: string
  day: number
  time: string
  weather: 'Sunny' | 'Cloudy' | 'Rainy'
  holiday: number
  vehicles: VehicleCounts
  top_k?: number
}

export interface RouteResponse {
  routes: RouteResult[]
}

export const apiClient = {
  health: async () => {
    const response = await api.get('/health')
    return response.data
  },

  predictTraffic: async (request: TrafficPredictionRequest) => {
    const response = await api.post<TrafficPredictionResponse>('/predict', request)
    return response.data
  },

  optimizeRoute: async (request: RouteRequest) => {
    const response = await api.post<RouteResponse>('/route', request)
    return response.data
  },
}

export default api

import React, { useState } from 'react'
import { TrafficPredictionRequest, VehicleCounts } from '@/lib/api'
import { Clock, MapPin, Cloud, AlertCircle } from 'lucide-react'

interface TrafficPredictionFormProps {
  onSubmit: (request: TrafficPredictionRequest) => Promise<void>
  loading?: boolean
  error?: string
}

export const TrafficPredictionForm: React.FC<TrafficPredictionFormProps> = ({ onSubmit, loading, error }) => {
  const [formData, setFormData] = useState<TrafficPredictionRequest>({
    day: 3,
    time: '09:30',
    weather: 'Sunny',
    road_type: 'Highway',
    holiday: 0,
    vehicles: {
      cars: 45,
      bikes: 20,
      buses: 8,
      trucks: 5,
    },
  })

  const handleVehicleChange = (type: keyof VehicleCounts, value: number) => {
    setFormData({
      ...formData,
      vehicles: { ...formData.vehicles, [type]: value },
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await onSubmit(formData)
  }

  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  const weathers = ['Sunny', 'Cloudy', 'Rainy'] as const
  const roadTypes = ['Highway', 'CityRoad', 'NarrowRoad'] as const

  return (
    <form onSubmit={handleSubmit} className="card space-y-6">
      <h2 className="text-2xl font-bold text-slate-800">Traffic Prediction</h2>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-red-700 text-sm">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Day Selection */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Day of Week</label>
          <select
            value={formData.day}
            onChange={(e) => setFormData({ ...formData, day: parseInt(e.target.value) })}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {days.map((day, idx) => (
              <option key={idx} value={idx + 1}>
                {day} ({idx + 1})
              </option>
            ))}
          </select>
        </div>

        {/* Time Selection */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
            <Clock className="w-4 h-4" /> Time (HH:MM)
          </label>
          <input
            type="time"
            value={formData.time}
            onChange={(e) => setFormData({ ...formData, time: e.target.value })}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Weather Selection */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
            <Cloud className="w-4 h-4" /> Weather
          </label>
          <select
            value={formData.weather}
            onChange={(e) => setFormData({ ...formData, weather: e.target.value as any })}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {weathers.map((w) => (
              <option key={w} value={w}>
                {w}
              </option>
            ))}
          </select>
        </div>

        {/* Road Type Selection */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
            <MapPin className="w-4 h-4" /> Road Type
          </label>
          <select
            value={formData.road_type}
            onChange={(e) => setFormData({ ...formData, road_type: e.target.value as any })}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {roadTypes.map((rt) => (
              <option key={rt} value={rt}>
                {rt}
              </option>
            ))}
          </select>
        </div>

        {/* Holiday Toggle */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Holiday</label>
          <select
            value={formData.holiday}
            onChange={(e) => setFormData({ ...formData, holiday: parseInt(e.target.value) })}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
      </div>

      {/* Vehicle Counts */}
      <div>
        <h3 className="text-lg font-semibold text-slate-800 mb-4">Vehicle Counts</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {(['cars', 'bikes', 'buses', 'trucks'] as const).map((type) => (
            <div key={type}>
              <label className="block text-sm font-medium text-slate-700 mb-2 capitalize">{type}</label>
              <input
                type="number"
                min="0"
                max="200"
                value={formData.vehicles[type]}
                onChange={(e) => handleVehicleChange(type, parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          ))}
        </div>
        <p className="text-sm text-slate-600 mt-2">
          Total: {Object.values(formData.vehicles).reduce((a, b) => a + b, 0)} vehicles
        </p>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? 'Predicting...' : 'Predict Traffic'}
      </button>
    </form>
  )
}

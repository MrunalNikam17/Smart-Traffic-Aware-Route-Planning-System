import React, { useState } from 'react'
import { RouteRequest, VehicleCounts } from '@/lib/api'
import { Navigation, AlertCircle } from 'lucide-react'

interface RouteOptimizationFormProps {
  onSubmit: (request: RouteRequest) => Promise<void>
  loading?: boolean
  error?: string
}

const NODES = ['A', 'B', 'C', 'D', 'E', 'F']

export const RouteOptimizationForm: React.FC<RouteOptimizationFormProps> = ({ onSubmit, loading, error }) => {
  const [formData, setFormData] = useState<RouteRequest>({
    start: 'A',
    goal: 'E',
    day: 3,
    time: '09:30',
    weather: 'Sunny',
    holiday: 0,
    vehicles: {
      cars: 30,
      bikes: 15,
      buses: 5,
      trucks: 3,
    },
    top_k: 3,
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

  return (
    <form onSubmit={handleSubmit} className="card space-y-6">
      <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
        <Navigation className="w-6 h-6" />
        Route Optimization
      </h2>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-red-700 text-sm">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Start Node */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Start Location</label>
          <select
            value={formData.start}
            onChange={(e) => setFormData({ ...formData, start: e.target.value })}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {NODES.map((node) => (
              <option key={node} value={node}>
                Node {node}
              </option>
            ))}
          </select>
        </div>

        {/* Goal Node */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Destination</label>
          <select
            value={formData.goal}
            onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {NODES.map((node) => (
              <option key={node} value={node}>
                Node {node}
              </option>
            ))}
          </select>
        </div>

        {/* Day */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Day</label>
          <select
            value={formData.day}
            onChange={(e) => setFormData({ ...formData, day: parseInt(e.target.value) })}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {days.map((day, idx) => (
              <option key={idx} value={idx + 1}>
                {day}
              </option>
            ))}
          </select>
        </div>

        {/* Time */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Time</label>
          <input
            type="time"
            value={formData.time}
            onChange={(e) => setFormData({ ...formData, time: e.target.value })}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Weather */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Weather</label>
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

        {/* Holiday */}
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
      </div>

      {/* Top K */}
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-2">Number of Routes to Show</label>
        <select
          value={formData.top_k}
          onChange={(e) => setFormData({ ...formData, top_k: parseInt(e.target.value) })}
          className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          {[1, 2, 3, 4, 5].map((k) => (
            <option key={k} value={k}>
              Top {k}
            </option>
          ))}
        </select>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-emerald-600 text-white py-3 rounded-lg font-semibold hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? 'Optimizing Routes...' : 'Find Best Routes'}
      </button>
    </form>
  )
}

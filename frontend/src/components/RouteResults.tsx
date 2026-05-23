import React from 'react'
import { RouteResponse } from '@/lib/api'
import { MapPin, TrendingDown, AlertCircle } from 'lucide-react'

interface RouteResultsProps {
  routes: RouteResponse | null
}

const trafficConfig = {
  1: { label: 'Light', color: 'text-traffic-light', bg: 'bg-traffic-light/10' },
  2: { label: 'Normal', color: 'text-traffic-normal', bg: 'bg-traffic-normal/10' },
  3: { label: 'Heavy', color: 'text-traffic-heavy', bg: 'bg-traffic-heavy/10' },
  4: { label: 'Congestion', color: 'text-traffic-congestion', bg: 'bg-traffic-congestion/10' },
}

export const RouteResults: React.FC<RouteResultsProps> = ({ routes }) => {
  if (!routes || routes.routes.length === 0) return null

  return (
    <div className="card space-y-6">
      <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
        <MapPin className="w-6 h-6" />
        Route Options ({routes.routes.length})
      </h2>

      <div className="space-y-4">
        {routes.routes.map((route, idx) => (
          <div key={idx} className={`border-2 ${idx === 0 ? 'border-emerald-400 bg-emerald-50' : 'border-slate-200'} rounded-lg p-4`}>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="font-semibold text-lg text-slate-800 flex items-center gap-2">
                  <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white font-bold text-sm">
                    {idx + 1}
                  </span>
                  {idx === 0 && (
                    <span className="inline-block px-2 py-1 bg-emerald-600 text-white text-xs font-semibold rounded">
                      BEST ROUTE
                    </span>
                  )}
                </h3>
                <p className="text-sm text-slate-600 mt-1">Path: {route.path.join(' → ')}</p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-emerald-600">{route.total_cost.toFixed(2)}</p>
                <p className="text-xs text-slate-600">Total Cost</p>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <p className="text-sm font-medium text-slate-700 mb-2">Edge Traffic Levels:</p>
                <div className="space-y-2">
                  {route.traffic_levels.map((level, edgeIdx) => {
                    const config = trafficConfig[level as 1 | 2 | 3 | 4]
                    return (
                      <div key={edgeIdx} className="flex items-center justify-between text-sm">
                        <span className="text-slate-600">
                          {route.path[edgeIdx]} → {route.path[edgeIdx + 1]}
                        </span>
                        <span className={`px-3 py-1 rounded-full font-medium ${config.bg} ${config.color}`}>{config.label}</span>
                      </div>
                    )
                  })}
                </div>
              </div>

              <div className="bg-slate-50 p-3 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600 font-medium">Average Traffic Level</span>
                  <span className="text-sm font-semibold text-slate-800">
                    {(route.traffic_levels.reduce((a, b) => a + b, 0) / route.traffic_levels.length).toFixed(1)}/4
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex gap-3">
        <TrendingDown className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <p className="text-sm text-blue-900">
          <strong>Recommendation:</strong> Route {routes.routes.findIndex((r) => r.total_cost === Math.min(...routes.routes.map((r) => r.total_cost))) + 1} offers
          the best balance of distance and traffic conditions.
        </p>
      </div>
    </div>
  )
}

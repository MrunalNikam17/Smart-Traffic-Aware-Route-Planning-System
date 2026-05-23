import React from 'react'
import { TrafficPredictionResponse } from '@/lib/api'
import { TrendingUp, CheckCircle } from 'lucide-react'

interface PredictionResultProps {
  prediction: TrafficPredictionResponse | null
}

const trafficLevelConfig = {
  1: { label: 'Light', color: 'bg-traffic-light', badge: 'traffic-badge-light' },
  2: { label: 'Normal', color: 'bg-traffic-normal', badge: 'traffic-badge-normal' },
  3: { label: 'Heavy', color: 'bg-traffic-heavy', badge: 'traffic-badge-heavy' },
  4: { label: 'Congestion', color: 'bg-traffic-congestion', badge: 'traffic-badge-congestion' },
}

export const PredictionResult: React.FC<PredictionResultProps> = ({ prediction }) => {
  if (!prediction) return null

  const config = trafficLevelConfig[prediction.traffic_level as 1 | 2 | 3 | 4]

  return (
    <div className="card space-y-4">
      <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
        <CheckCircle className="w-6 h-6 text-green-600" />
        Prediction Result
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <p className="text-sm font-medium text-slate-600">Traffic Level</p>
          <div className={`${config.badge} text-2xl`}>{config.label}</div>
          <div className="flex gap-1">
            {[1, 2, 3, 4].map((level) => (
              <div
                key={level}
                className={`h-2 flex-1 rounded ${
                  level <= prediction.traffic_level ? trafficLevelConfig[level as 1 | 2 | 3 | 4].color : 'bg-slate-200'
                }`}
              />
            ))}
          </div>
        </div>

        <div className="space-y-2">
          <p className="text-sm font-medium text-slate-600">Confidence</p>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-bold text-blue-600">{(prediction.confidence * 100).toFixed(1)}%</span>
            <TrendingUp className="w-5 h-5 text-blue-600 mb-1" />
          </div>
          <div className="w-full bg-slate-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all"
              style={{ width: `${prediction.confidence * 100}%` }}
            />
          </div>
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-900">
          <strong>Analysis:</strong> Current traffic is{' '}
          {prediction.traffic_level <= 2 ? 'flowing well' : prediction.traffic_level === 3 ? 'moderate' : 'experiencing congestion'}.
          Plan your route accordingly.
        </p>
      </div>
    </div>
  )
}

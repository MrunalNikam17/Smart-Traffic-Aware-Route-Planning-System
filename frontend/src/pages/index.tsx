import React, { useState, useEffect } from 'react'
import Head from 'next/head'
import { Header } from '../components/Header'
import { TrafficPredictionForm } from '../components/TrafficPredictionForm'
import { PredictionResult } from '../components/PredictionResult'
import { RouteOptimizationForm } from '../components/RouteOptimizationForm'
import { RouteResults } from '../components/RouteResults'
import { apiClient, TrafficPredictionRequest, TrafficPredictionResponse, RouteRequest, RouteResponse } from '../lib/api'
import { AlertCircle, CheckCircle } from 'lucide-react'

export default function Dashboard() {
  const [prediction, setPrediction] = useState<TrafficPredictionResponse | null>(null)
  const [routes, setRoutes] = useState<RouteResponse | null>(null)
  const [predictionLoading, setPredictionLoading] = useState(false)
  const [routesLoading, setRoutesLoading] = useState(false)
  const [predictionError, setPredictionError] = useState<string>('')
  const [routesError, setRoutesError] = useState<string>('')
  const [apiStatus, setApiStatus] = useState<'loading' | 'healthy' | 'error'>('loading')

  // Check API health on mount
  useEffect(() => {
    checkApiHealth()
  }, [])

  const checkApiHealth = async () => {
    try {
      await apiClient.health()
      setApiStatus('healthy')
    } catch (error) {
      setApiStatus('error')
    }
  }

  const handlePredictTraffic = async (request: TrafficPredictionRequest) => {
    setPredictionLoading(true)
    setPredictionError('')
    try {
      const result = await apiClient.predictTraffic(request)
      setPrediction(result)
    } catch (error: any) {
      setPredictionError(error.response?.data?.detail || 'Failed to get prediction. Please check the backend.')
      setPrediction(null)
    } finally {
      setPredictionLoading(false)
    }
  }

  const handleOptimizeRoute = async (request: RouteRequest) => {
    setRoutesLoading(true)
    setRoutesError('')
    try {
      const result = await apiClient.optimizeRoute(request)
      setRoutes(result)
    } catch (error: any) {
      setRoutesError(error.response?.data?.detail || 'Failed to optimize route. Please check the backend.')
      setRoutes(null)
    } finally {
      setRoutesLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>Traffic Intelligence System - Dashboard</title>
        <meta name="description" content="Real-time traffic prediction and route optimization" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <Header />

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* API Status */}
        <div className="mb-6">
          {apiStatus === 'loading' && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex gap-3">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600" />
              <p className="text-blue-900">Connecting to backend...</p>
            </div>
          )}
          {apiStatus === 'error' && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <p className="text-red-900">
                <strong>Backend Connection Error:</strong> Make sure the FastAPI backend is running at{' '}
                {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
              </p>
            </div>
          )}
          {apiStatus === 'healthy' && (
            <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4 flex gap-3">
              <CheckCircle className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
              <p className="text-emerald-900">Connected to Traffic Intelligence Backend</p>
            </div>
          )}
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Forms */}
          <div className="space-y-8">
            <TrafficPredictionForm onSubmit={handlePredictTraffic} loading={predictionLoading} error={predictionError} />
            <RouteOptimizationForm onSubmit={handleOptimizeRoute} loading={routesLoading} error={routesError} />
          </div>

          {/* Right Column - Results */}
          <div className="space-y-8">
            {!prediction && !routes ? (
              <div className="card text-center py-12">
                <p className="text-slate-600 text-lg">Fill out a form on the left to get started</p>
              </div>
            ) : (
              <>
                {prediction && <PredictionResult prediction={prediction} />}
                {routes && <RouteResults routes={routes} />}
              </>
            )}
          </div>
        </div>
      </main>

      <footer className="mt-16 bg-slate-100 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-slate-600 text-sm">
          <p>Traffic Intelligence System © 2024 | Powered by AI & FastAPI</p>
        </div>
      </footer>
    </>
  )
}

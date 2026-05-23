# Traffic Intelligence System - Frontend

Modern React/Next.js dashboard for real-time traffic prediction and route optimization.

## Features

- **Traffic Prediction**: Real-time traffic level prediction with confidence scores
- **Route Optimization**: Find the best routes with traffic-aware cost calculation
- **Interactive Dashboard**: Modern UI with Tailwind CSS
- **API Integration**: Seamless integration with FastAPI backend

## Setup

```bash
# Install dependencies
npm install

# Set environment variables
# Create a .env.local file (if backend is not at localhost:8000)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

## Project Structure

- `src/pages/` - Next.js pages
- `src/components/` - React components
- `src/lib/` - API client and utilities
- `src/styles/` - Global styles and Tailwind config

## Requirements

- Node.js 16+
- Backend running at http://localhost:8000

## API Endpoints Used

- `GET /health` - Health check
- `POST /predict` - Traffic prediction
- `POST /route` - Route optimization

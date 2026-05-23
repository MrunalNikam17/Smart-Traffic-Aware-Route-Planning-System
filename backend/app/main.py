from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.traffic import router as traffic_router
from app.routes.realtime import router as realtime_router

app = FastAPI(
    title="Real-Time Traffic Intelligence API",
    description="Backend service for traffic prediction, route optimization, and live simulation.",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(traffic_router)
app.include_router(realtime_router)


@app.get("/")
def root():
    return {"message": "Traffic Intelligence Backend Running"}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "traffic-intelligence-backend"
    }
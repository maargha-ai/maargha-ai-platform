# app/monitoring/health.py
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import asyncio
import time
from app.monitoring.logger import performance_monitor, monitoring_logger

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "maargha-orchestrator"
    }

@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with system metrics"""
    try:
        # Test database connection
        db_status = await test_database_connection()
        
        # Test external services
        external_services = await test_external_services()
        
        # Get performance metrics
        metrics = performance_monitor.get_metrics()
        
        overall_status = "healthy"
        if db_status != "healthy" or any(status != "healthy" for status in external_services.values()):
            overall_status = "degraded"
        
        return {
            "status": overall_status,
            "timestamp": time.time(),
            "service": "maargha-orchestrator",
            "checks": {
                "database": db_status,
                "external_services": external_services
            },
            "metrics": metrics
        }
        
    except Exception as e:
        monitoring_logger.error("Health check failed", error=e)
        raise HTTPException(status_code=503, detail="Service unavailable")

async def test_database_connection() -> str:
    """Test database connectivity"""
    try:
        from app.db.database import engine
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        return "healthy"
    except Exception as e:
        monitoring_logger.error("Database health check failed", error=e)
        return "unhealthy"

async def test_external_services() -> Dict[str, str]:
    """Test connectivity to external services"""
    services = {}
    
    # Test Groq API
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("https://api.groq.com/openai/v1/models")
            services["groq_api"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception as e:
        monitoring_logger.warning("Groq API health check failed", extra={"error": str(e)})
        services["groq_api"] = "unhealthy"
    
    return services

@router.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get application performance metrics"""
    return performance_monitor.get_metrics()

@router.get("/readiness")
async def readiness_check() -> Dict[str, Any]:
    """Readiness check for Kubernetes/container orchestration"""
    metrics = performance_monitor.get_metrics()
    
    # Consider service ready if we have processed at least one request
    is_ready = metrics["total_requests"] > 0
    
    return {
        "status": "ready" if is_ready else "not_ready",
        "timestamp": time.time(),
        "checks": {
            "has_processed_requests": is_ready,
            "active_connections": metrics["active_connections"]
        }
    }

@router.get("/liveness")
async def liveness_check() -> Dict[str, Any]:
    """Liveness check for Kubernetes/container orchestration"""
    return {
        "status": "alive",
        "timestamp": time.time(),
        "service": "maargha-orchestrator"
    }

# user_service/monitoring/health.py
import time
from typing import Any, Dict

from django.http import JsonResponse

from user_service.monitoring.logger import monitoring_logger, performance_monitor


def health_check() -> Dict[str, Any]:
    """Basic health check endpoint"""
    return JsonResponse(
        {
            "status": "healthy",
            "timestamp": time.time(),
            "service": "maargha-user-service",
        }
    )


def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with system metrics"""
    try:
        # Test database connection
        db_status = test_database_connection()

        # Get performance metrics
        metrics = performance_monitor.get_metrics()

        overall_status = "healthy"
        if db_status != "healthy":
            overall_status = "degraded"

        return JsonResponse(
            {
                "status": overall_status,
                "timestamp": time.time(),
                "service": "maargha-user-service",
                "checks": {"database": db_status},
                "metrics": metrics,
            }
        )

    except Exception as e:
        monitoring_logger.error("Health check failed", error=e)
        return JsonResponse({"status": "unhealthy", "error": str(e)}, status=503)


def test_database_connection() -> str:
    """Test database connectivity"""
    try:
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return "healthy"
    except Exception as e:
        monitoring_logger.error("Database health check failed", error=e)
        return "unhealthy"


def get_metrics() -> Dict[str, Any]:
    """Get application performance metrics"""
    return performance_monitor.get_metrics()


def readiness_check() -> Dict[str, Any]:
    """Readiness check for Kubernetes/container orchestration"""
    metrics = performance_monitor.get_metrics()

    # Consider service ready if we have processed at least one request
    is_ready = metrics["total_requests"] > 0

    return JsonResponse(
        {
            "status": "ready" if is_ready else "not_ready",
            "timestamp": time.time(),
            "checks": {
                "has_processed_requests": is_ready,
                "active_connections": 0,  # Django doesn't have WebSocket connections
            },
        }
    )


def liveness_check() -> Dict[str, Any]:
    """Liveness check for Kubernetes/container orchestration"""
    return JsonResponse(
        {"status": "alive", "timestamp": time.time(), "service": "maargha-user-service"}
    )

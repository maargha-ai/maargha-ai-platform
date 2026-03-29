# user_service/monitoring/logger.py
import logging
import time
from typing import Any, Dict

# Create loggers
monitoring_logger = logging.getLogger("monitoring")
performance_monitor = logging.getLogger("performance")

def log_performance(func_name: str, duration: float) -> None:
    """Log performance metrics"""
    performance_monitor.info(f"{func_name} took {duration:.2f}s")

def get_metrics() -> Dict[str, Any]:
    """Get basic metrics"""
    return {
        "timestamp": time.time(),
        "status": "healthy"
    }

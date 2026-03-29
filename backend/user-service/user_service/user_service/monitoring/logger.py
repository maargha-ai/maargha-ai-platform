# user_service/monitoring/logger.py
import logging
import time
from typing import Any, Dict
from contextlib import contextmanager

# Create loggers
monitoring_logger = logging.getLogger("monitoring")
performance_monitor = logging.getLogger("performance")
user_service_logger = logging.getLogger("user_service")

def log_performance(func_name: str, duration: float) -> None:
    """Log performance metrics"""
    performance_monitor.info(f"{func_name} took {duration:.2f}s")

def get_metrics() -> Dict[str, Any]:
    """Get basic metrics"""
    return {
        "timestamp": time.time(),
        "status": "healthy"
    }

# Mock classes for compatibility with tests
class PerformanceMonitor:
    """Mock PerformanceMonitor class for test compatibility"""
    
    def __init__(self):
        self.start_time = None
    
    def start(self):
        self.start_time = time.time()
    
    def stop(self):
        if self.start_time:
            duration = time.time() - self.start_time
            log_performance("operation", duration)
            return duration
        return 0

class StructuredLogger:
    """Mock StructuredLogger class for test compatibility"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def info(self, message: str, **kwargs):
        self.logger.info(message)
    
    def error(self, message: str, **kwargs):
        self.logger.error(message)
    
    def warning(self, message: str, **kwargs):
        self.logger.warning(message)

@contextmanager
def log_function_call(func_name: str):
    """Context manager for logging function calls"""
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        log_performance(func_name, duration)

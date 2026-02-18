# user_service/monitoring/logger.py
import logging
import json
import time
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
import structlog

class StructuredLogger:
    """Enhanced logger with structured logging for production monitoring"""
    
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = structlog.get_logger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message with optional structured data"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO",
            "message": message,
            **(extra or {})
        }
        self.logger.info(message, extra=log_data)
    
    def error(self, message: str, error: Exception = None, extra: Dict[str, Any] = None):
        """Log error message with exception details"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "ERROR",
            "message": message,
            **(extra or {})
        }
        
        if error:
            log_data["error"] = {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            }
        
        self.logger.error(message, extra=log_data)
    
    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log warning message with optional structured data"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "WARNING",
            "message": message,
            **(extra or {})
        }
        self.logger.warning(message, extra=log_data)
    
    def debug(self, message: str, extra: Dict[str, Any] = None):
        """Log debug message with optional structured data"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "DEBUG",
            "message": message,
            **(extra or {})
        }
        self.logger.debug(message, extra=log_data)

# Create logger instances for different services
user_service_logger = StructuredLogger("user_service")
api_logger = StructuredLogger("user_service_api")
monitoring_logger = StructuredLogger("user_service_monitoring")

def log_function_call(func):
    """Decorator to log function calls with timing and error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function_name = f"{func.__module__}.{func.__name__}"
        
        try:
            user_service_logger.info(
                f"Function call started",
                extra={
                    "function": function_name,
                    "args_count": len(args),
                    "kwargs": list(kwargs.keys())
                }
            )
            
            result = func(*args, **kwargs)
            
            execution_time = time.time() - start_time
            user_service_logger.info(
                f"Function call completed",
                extra={
                    "function": function_name,
                    "execution_time": round(execution_time, 3),
                    "success": True
                }
            )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            user_service_logger.error(
                f"Function call failed",
                error=e,
                extra={
                    "function": function_name,
                    "execution_time": round(execution_time, 3),
                    "success": False
                }
            )
            raise
    
    return wrapper

class PerformanceMonitor:
    """Monitor application performance metrics"""
    
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "total_errors": 0,
            "total_db_queries": 0,
            "response_times": [],
            "error_types": {}
        }
    
    def record_request(self, response_time: float, status_code: int):
        """Record HTTP request metrics"""
        self.metrics["total_requests"] += 1
        self.metrics["response_times"].append(response_time)
        
        # Keep only last 1000 response times for memory efficiency
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]
        
        if status_code >= 400:
            self.metrics["total_errors"] += 1
    
    def record_db_query(self, query_time: float):
        """Record database query metrics"""
        self.metrics["total_db_queries"] += 1
        # Could add query_time tracking here
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        response_times = self.metrics["response_times"]
        
        return {
            "total_requests": self.metrics["total_requests"],
            "total_errors": self.metrics["total_errors"],
            "total_db_queries": self.metrics["total_db_queries"],
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "max_response_time": max(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "error_rate": self.metrics["total_errors"] / max(1, self.metrics["total_requests"]) * 100
        }

class LoggingMiddleware(MiddlewareMixin):
    """Django middleware for structured logging"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def process_request(self, request):
        start_time = time.time()
        
        # Log request
        api_logger.info(
            f"HTTP request received",
            extra={
                "method": request.method,
                "url": request.build_absolute_uri(),
                "client_ip": self.get_client_ip(request),
                "user_agent": request.META.get("HTTP_USER_AGENT", "unknown")
            }
        )
        
        response = self.get_response(request)
        
        # Log response
        process_time = time.time() - start_time
        api_logger.info(
            f"HTTP response sent",
            extra={
                "method": request.method,
                "url": request.build_absolute_uri(),
                "status_code": response.status_code,
                "process_time": round(process_time, 3)
            }
        )
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip or "unknown"

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

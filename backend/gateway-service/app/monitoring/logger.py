# app/monitoring/logger.py
import json
import logging
import time
import traceback
from datetime import datetime
from functools import wraps
from typing import Any, Dict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class StructuredLogger:
    """Enhanced logger with structured logging for production monitoring"""

    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Create console handler with formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level.upper()))

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message with optional structured data"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO",
            "message": message,
            **(extra or {}),
        }
        self.logger.info(json.dumps(log_data))

    def error(
        self, message: str, error: Exception = None, extra: Dict[str, Any] = None
    ):
        """Log error message with exception details"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "ERROR",
            "message": message,
            **(extra or {}),
        }

        if error:
            log_data["error"] = {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc(),
            }

        self.logger.error(json.dumps(log_data))

    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log warning message with optional structured data"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "WARNING",
            "message": message,
            **(extra or {}),
        }
        self.logger.warning(json.dumps(log_data))

    def debug(self, message: str, extra: Dict[str, Any] = None):
        """Log debug message with optional structured data"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "DEBUG",
            "message": message,
            **(extra or {}),
        }
        self.logger.debug(json.dumps(log_data))


# Create logger instances for different services
gateway_logger = StructuredLogger("gateway")
api_logger = StructuredLogger("gateway_api")
monitoring_logger = StructuredLogger("gateway_monitoring")


def log_function_call(func):
    """Decorator to log function calls with timing and error handling"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        function_name = f"{func.__module__}.{func.__name__}"

        try:
            gateway_logger.info(
                "Function call started",
                extra={
                    "function": function_name,
                    "args_count": len(args),
                    "kwargs": list(kwargs.keys()),
                },
            )

            result = await func(*args, **kwargs)

            execution_time = time.time() - start_time
            gateway_logger.info(
                "Function call completed",
                extra={
                    "function": function_name,
                    "execution_time": round(execution_time, 3),
                    "success": True,
                },
            )

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            gateway_logger.error(
                "Function call failed",
                error=e,
                extra={
                    "function": function_name,
                    "execution_time": round(execution_time, 3),
                    "success": False,
                },
            )
            raise

    return wrapper


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and responses"""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        api_logger.info(
            "HTTP request received",
            extra={
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown"),
            },
        )

        try:
            response = await call_next(request)

            # Log response
            process_time = time.time() - start_time
            api_logger.info(
                "HTTP response sent",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "process_time": round(process_time, 3),
                },
            )

            return response

        except Exception as e:
            process_time = time.time() - start_time
            api_logger.error(
                "HTTP request failed",
                error=e,
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "process_time": round(process_time, 3),
                },
            )
            raise


class PerformanceMonitor:
    """Monitor application performance metrics"""

    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "total_errors": 0,
            "total_websocket_connections": 0,
            "active_connections": 0,
            "response_times": [],
            "error_types": {},
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

    def record_websocket_connection(self):
        """Record new WebSocket connection"""
        self.metrics["total_websocket_connections"] += 1
        self.metrics["active_connections"] += 1

        monitoring_logger.info(
            "WebSocket connection established",
            extra={
                "total_connections": self.metrics["total_websocket_connections"],
                "active_connections": self.metrics["active_connections"],
            },
        )

    def record_websocket_disconnection(self):
        """Record WebSocket disconnection"""
        self.metrics["active_connections"] = max(
            0, self.metrics["active_connections"] - 1
        )

        monitoring_logger.info(
            "WebSocket connection closed",
            extra={"active_connections": self.metrics["active_connections"]},
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        response_times = self.metrics["response_times"]

        return {
            "total_requests": self.metrics["total_requests"],
            "total_errors": self.metrics["total_errors"],
            "total_websocket_connections": self.metrics["total_websocket_connections"],
            "active_connections": self.metrics["active_connections"],
            "avg_response_time": (
                sum(response_times) / len(response_times) if response_times else 0
            ),
            "max_response_time": max(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "error_rate": self.metrics["total_errors"]
            / max(1, self.metrics["total_requests"])
            * 100,
        }


# Global performance monitor instance
performance_monitor = PerformanceMonitor()

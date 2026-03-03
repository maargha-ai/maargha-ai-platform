# user_service/monitoring/logger.py

import logging
import time
import traceback
from datetime import datetime
from functools import wraps
from typing import Any, Dict

import structlog
from django.utils.deprecation import MiddlewareMixin


# ---------------------------------------------------
# STRUCTLOG CONFIGURATION (GLOBAL SETUP)
# ---------------------------------------------------


def setup_logging(level: str = "INFO"):
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, level.upper()),
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
    )


setup_logging("INFO")


# ---------------------------------------------------
# STRUCTURED LOGGER CLASS
# ---------------------------------------------------


class StructuredLogger:
    def __init__(self, name: str):
        self.logger = structlog.get_logger(name)

    def info(self, message: str, extra: Dict[str, Any] = None):
        self.logger.info(message, **(extra or {}))

    def error(
        self, message: str, error: Exception = None, extra: Dict[str, Any] = None
    ):
        log_data = extra or {}

        if error:
            log_data["error"] = {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc(),
            }

        self.logger.error(message, **log_data)

    def warning(self, message: str, extra: Dict[str, Any] = None):
        self.logger.warning(message, **(extra or {}))

    def debug(self, message: str, extra: Dict[str, Any] = None):
        self.logger.debug(message, **(extra or {}))


# Logger instances
user_service_logger = StructuredLogger("user_service")
api_logger = StructuredLogger("user_service_api")
monitoring_logger = StructuredLogger("user_service_monitoring")


# ---------------------------------------------------
# FUNCTION CALL DECORATOR
# ---------------------------------------------------


def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function_name = f"{func.__module__}.{func.__name__}"

        try:
            user_service_logger.info(
                "Function call started",
                {
                    "function": function_name,
                    "args_count": len(args),
                    "kwargs": list(kwargs.keys()),
                },
            )

            result = func(*args, **kwargs)

            execution_time = time.time() - start_time
            user_service_logger.info(
                "Function call completed",
                {
                    "function": function_name,
                    "execution_time": round(execution_time, 3),
                    "success": True,
                },
            )

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            user_service_logger.error(
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


# ---------------------------------------------------
# PERFORMANCE MONITOR
# ---------------------------------------------------


class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "total_errors": 0,
            "total_db_queries": 0,
            "response_times": [],
        }

    def record_request(self, response_time: float, status_code: int):
        self.metrics["total_requests"] += 1
        self.metrics["response_times"].append(response_time)

        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]

        if status_code >= 400:
            self.metrics["total_errors"] += 1

    def get_metrics(self) -> Dict[str, Any]:
        times = self.metrics["response_times"]

        return {
            "total_requests": self.metrics["total_requests"],
            "total_errors": self.metrics["total_errors"],
            "avg_response_time": sum(times) / len(times) if times else 0,
        }


performance_monitor = PerformanceMonitor()


# ---------------------------------------------------
# DJANGO LOGGING MIDDLEWARE
# ---------------------------------------------------


class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.time()

        api_logger.info(
            "HTTP request received",
            {
                "method": request.method,
                "url": request.build_absolute_uri(),
                "client_ip": request.META.get("REMOTE_ADDR"),
            },
        )

    def process_response(self, request, response):
        if hasattr(request, "_start_time"):
            duration = time.time() - request._start_time

            api_logger.info(
                "HTTP response sent",
                {
                    "status_code": response.status_code,
                    "duration": round(duration, 3),
                },
            )

        return response
# tests/test_user_service_logger.py
import time
from unittest.mock import Mock, patch

import pytest

from user_service.monitoring.logger import (
    PerformanceMonitor,
    StructuredLogger,
    log_function_call,
)


class TestUserServiceStructuredLogger:
    """Test cases for Django StructuredLogger"""

    def test_logger_initialization(self):
        """Test logger initialization"""
        logger = StructuredLogger("test_user_service_logger")
        assert logger.logger is not None

    def test_info_logging(self):
        """Test info logging with structured data"""
        logger = StructuredLogger("test_user_service_logger")

        with patch.object(logger, "logger") as mock_logger:
            logger.info("Test message", extra={"test": "data"})
            mock_logger.info.assert_called_once_with("Test message", test="data")

    def test_error_logging_with_exception(self):
        """Test error logging with exception"""
        logger = StructuredLogger("test_user_service_logger")

        try:
            raise ValueError("Test error")
        except Exception as e:
            with patch.object(logger, "logger") as mock_logger:
                logger.error("Error occurred", error=e, extra={"context": "test"})

                # Verify error was called
                mock_logger.error.assert_called_once()
                call_kwargs = mock_logger.error.call_args[1]
                assert "error" in call_kwargs
                assert call_kwargs["error"]["type"] == "ValueError"
                assert call_kwargs["error"]["message"] == "Test error"


class TestUserServicePerformanceMonitor:
    """Test cases for Django PerformanceMonitor"""

    def test_initialization(self):
        """Test performance monitor initialization"""
        monitor = PerformanceMonitor()

        assert monitor.metrics["total_requests"] == 0
        assert monitor.metrics["total_errors"] == 0
        assert monitor.metrics["total_db_queries"] == 0
        assert monitor.metrics["response_times"] == []

    def test_record_request(self):
        """Test request recording"""
        monitor = PerformanceMonitor()

        monitor.record_request(0.5, 200)
        monitor.record_request(1.0, 404)

        assert monitor.metrics["total_requests"] == 2
        assert monitor.metrics["total_errors"] == 1
        assert monitor.metrics["response_times"] == [0.5, 1.0]

    def test_get_metrics(self):
        """Test get_metrics returns correct values"""
        monitor = PerformanceMonitor()

        monitor.record_request(0.1, 200)
        monitor.record_request(0.2, 200)

        metrics = monitor.get_metrics()
        assert metrics["total_requests"] == 2
        assert metrics["total_errors"] == 0
        assert metrics["avg_response_time"] == pytest.approx(0.15)


class TestUserServiceLoggingMiddleware:
    """Test cases for Django LoggingMiddleware"""

    def test_middleware_logs_request_response(self):
        """Test middleware logs HTTP requests and responses"""
        from django.http import HttpRequest, HttpResponse

        from user_service.monitoring.logger import LoggingMiddleware

        # Create mock request and response
        mock_request = Mock(spec=HttpRequest)
        mock_request.method = "GET"
        mock_request.build_absolute_uri.return_value = "http://test.com/api/test"
        mock_request.META = {
            "REMOTE_ADDR": "127.0.0.1",
            "HTTP_USER_AGENT": "test-agent",
        }

        mock_response = Mock(spec=HttpResponse)
        mock_response.status_code = 200

        # Test middleware
        middleware = LoggingMiddleware(get_response=lambda r: mock_response)

        with patch("user_service.monitoring.logger.api_logger.info") as mock_log:
            # Process the request through middleware
            middleware.process_request(mock_request)

            # Verify logging was called
            assert mock_log.call_count >= 1


class TestUserServiceFunctionDecorator:
    """Test cases for Django function decorator"""

    def test_successful_function_call(self):
        """Test decorator logs successful function calls"""

        @log_function_call
        def test_function(x, y):
            return x + y

        with patch(
            "user_service.monitoring.logger.user_service_logger.info"
        ) as mock_log:
            result = test_function(2, 3)

            assert result == 5
            assert mock_log.call_count == 2  # Start and completion

    def test_failed_function_call(self):
        """Test decorator logs failed function calls"""

        @log_function_call
        def failing_function():
            raise ValueError("Test error")

        with patch(
            "user_service.monitoring.logger.user_service_logger.info"
        ) as mock_log:
            with patch(
                "user_service.monitoring.logger.user_service_logger.error"
            ) as mock_error:
                with pytest.raises(ValueError):
                    failing_function()

                assert mock_log.call_count == 1  # Start call
                assert mock_error.call_count == 1  # Error call


if __name__ == "__main__":
    pytest.main([__file__])

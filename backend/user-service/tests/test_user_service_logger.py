# tests/test_user_service_logger.py
import json
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
        logger = StructuredLogger("test_user_service_logger", "DEBUG")
        assert logger.logger.name == "test_user_service_logger"
        assert logger.logger.level == 10  # DEBUG level

    def test_info_logging(self):
        """Test info logging with structured data"""
        logger = StructuredLogger("test_user_service_logger")

        with patch("json.dumps") as mock_dumps:
            mock_dumps.return_value = '{"test": "data"}'
            logger.info("Test message", extra={"test": "data"})

            mock_dumps.assert_called_once()

    def test_error_logging_with_exception(self):
        """Test error logging with exception"""
        logger = StructuredLogger("test_user_service_logger")

        try:
            raise ValueError("Test error")
        except Exception as e:
            with patch("json.dumps") as mock_dumps:
                with patch("traceback.format_exc") as mock_format:
                    mock_format.return_value = "Traceback"
                    logger.error("Error occurred", error=e, extra={"context": "test"})

                    # Verify error details are included
                    call_args = mock_dumps.call_args[0][0]
                    assert "error" in call_args
                    assert call_args["error"]["type"] == "ValueError"
                    assert call_args["error"]["message"] == "Test error"


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

    def test_record_db_query(self):
        """Test database query recording"""
        monitor = PerformanceMonitor()

        monitor.record_db_query(0.2)
        monitor.record_db_query(0.3)

        assert monitor.metrics["total_db_queries"] == 2


@pytest.mark.django_db
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
            # Simulate middleware behavior
            start_time = time.time()
            time.sleep(0.01)  # Small delay
            process_time = time.time() - start_time

            # Verify logging calls would be made
            assert mock_log.call_count >= 1


@pytest.mark.django_db
class TestUserServiceFunctionDecorator:
    """Test cases for Django function decorator"""

    def test_successful_function_call(self):
        """Test decorator logs successful function calls"""

        @log_function_call
        def testFunction(x, y):
            return x + y

        with patch(
            "user_service.monitoring.logger.user_service_logger.info"
        ) as mock_log:
            result = TestFunction(2, 3)

            assert result == 5
            assert mock_log.call_count == 2  # Start and completion

            # Verify start call
            start_call = mock_log.call_args_list[0]
            assert "Function call started" in start_call[0][0]

            # Verify completion call
            completion_call = mock_log.call_args_list[1]
            assert "Function call completed" in completion_call[0][0]
            assert completion_call[1]["extra"]["success"] is True

    def test_failed_function_call(self):
        """Test decorator logs failed function calls"""

        @log_function_call
        def failingFunction():
            raise ValueError("Test error")

        with patch(
            "user_service.monitoring.logger.user_service_logger.info"
        ) as mock_log:
            with patch(
                "user_service.monitoring.logger.user_service_logger.error"
            ) as mock_error:
                with pytest.raises(ValueError):
                    failingFunction()

                assert mock_log.call_count == 1  # Start call
                assert mock_error.call_count == 1  # Error call

                # Verify error logging
                error_call = mock_error.call_args_list[0]
                assert "Function call failed" in error_call[0][0]
                assert error_call[1]["extra"]["success"] is False


if __name__ == "__main__":
    pytest.main([__file__])

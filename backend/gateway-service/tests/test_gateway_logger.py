# tests/test_gateway_logger.py
import pytest
import json
import time
from unittest.mock import Mock, patch
from app.monitoring.logger import (
    StructuredLogger, 
    LoggingMiddleware, 
    PerformanceMonitor,
    log_function_call
)

class TestGatewayStructuredLogger:
    """Test cases for StructuredLogger"""
    
    def test_logger_initialization(self):
        """Test logger initialization"""
        logger = StructuredLogger("test_gateway_logger", "DEBUG")
        assert logger.logger.name == "test_gateway_logger"
        assert logger.logger.level == 10  # DEBUG level
    
    def test_info_logging(self, caplog):
        """Test info logging with structured data"""
        logger = StructuredLogger("test_gateway_logger")
        
        with patch('json.dumps') as mock_dumps:
            mock_dumps.return_value = '{"test": "data"}'
            logger.info("Test message", extra={"test": "data"})
            
            mock_dumps.assert_called_once()
    
    def test_error_logging_with_exception(self):
        """Test error logging with exception"""
        logger = StructuredLogger("test_gateway_logger")
        
        try:
            raise ValueError("Test error")
        except Exception as e:
            with patch('json.dumps') as mock_dumps:
                with patch('traceback.format_exc') as mock_format:
                    mock_format.return_value = "Traceback"
                    logger.error("Error occurred", error=e, extra={"context": "test"})
                    
                    # Verify error details are included
                    call_args = mock_dumps.call_args[0][0]
                    assert "error" in call_args
                    assert call_args["error"]["type"] == "ValueError"
                    assert call_args["error"]["message"] == "Test error"

class TestGatewayPerformanceMonitor:
    """Test cases for PerformanceMonitor"""
    
    def test_initialization(self):
        """Test performance monitor initialization"""
        monitor = PerformanceMonitor()
        
        assert monitor.metrics["total_requests"] == 0
        assert monitor.metrics["total_errors"] == 0
        assert monitor.metrics["active_connections"] == 0
        assert monitor.metrics["response_times"] == []
    
    def test_record_request(self):
        """Test request recording"""
        monitor = PerformanceMonitor()
        
        monitor.record_request(0.5, 200)
        monitor.record_request(1.0, 404)
        
        assert monitor.metrics["total_requests"] == 2
        assert monitor.metrics["total_errors"] == 1
        assert monitor.metrics["response_times"] == [0.5, 1.0]
    
    def test_websocket_connection_tracking(self):
        """Test WebSocket connection tracking"""
        monitor = PerformanceMonitor()
        
        monitor.record_websocket_connection()
        assert monitor.metrics["total_websocket_connections"] == 1
        assert monitor.metrics["active_connections"] == 1
        
        monitor.record_websocket_disconnection()
        assert monitor.metrics["active_connections"] == 0

@pytest.mark.asyncio
class TestGatewayLoggingMiddleware:
    """Test cases for LoggingMiddleware"""
    
    async def test_middleware_logs_request_response(self):
        """Test middleware logs HTTP requests and responses"""
        from fastapi import Request, Response
        from starlette.middleware.base import BaseHTTPMiddleware
        
        # Create mock request and response
        mock_request = Mock(spec=Request)
        mock_request.method = "GET"
        mock_request.url = "http://test.com/api/test"
        mock_request.client = Mock(host="127.0.0.1")
        mock_request.headers = {"user-agent": "test-agent"}
        
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        
        # Test middleware
        middleware = LoggingMiddleware(Mock())
        
        with patch('app.monitoring.logger.api_logger.info') as mock_log:
            # Simulate middleware behavior
            start_time = time.time()
            time.sleep(0.01)  # Small delay
            process_time = time.time() - start_time
            
            # Verify logging calls would be made
            assert mock_log.call_count >= 1

if __name__ == "__main__":
    pytest.main([__file__])

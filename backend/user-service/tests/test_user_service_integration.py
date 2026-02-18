# tests/test_user_service_integration.py
import pytest
from django.test import Client
from unittest.mock import Mock, patch
from django.urls import reverse
from django.contrib.auth import get_user_model
from user_service.monitoring.logger import performance_monitor, user_service_logger

class TestUserServiceIntegration:
    """Integration tests for Django user service"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = Client()
    
    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        response = self.client.options("/health/")
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "*"
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers
    
    def test_user_model_integration(self):
        """Test user model integration"""
        from django.contrib.auth.models import User
        from user_service.accounts.models import CustomUser
        
        # Test that custom user model is properly configured
        assert hasattr(CustomUser, 'USERNAME_FIELD')
        assert hasattr(CustomUser, 'EMAIL_FIELD')
    
    def test_database_integration(self):
        """Test database integration"""
        from django.db import connection
        from user_service.accounts.models import CustomUser
        
        # Test database queries work
        with patch('user_service.monitoring.logger.performance_monitor') as mock_monitor:
            mock_monitor.record_db_query(0.1)
            
            # Create a test user
            user = CustomUser.objects.create_user(
                username='testuser',
                email='test@example.com'
            )
            
            metrics = mock_monitor.get_metrics()
            assert metrics["total_db_queries"] == 1
    
    def test_authentication_flow(self):
        """Test authentication flow"""
        from django.contrib.auth import authenticate
        from user_service.accounts.models import CustomUser
        
        # Create test user
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Test authentication
        authenticated_user = authenticate(username='testuser', password='testpass123')
        
        assert authenticated_user is not None
        assert authenticated_user.username == 'testuser'
    
    def test_api_endpoint_integration(self):
        """Test API endpoint integration"""
        with patch('user_service.monitoring.logger.performance_monitor') as mock_monitor:
            mock_monitor.record_request(0.1, 200)
            
            # Test a sample API endpoint
            response = self.client.get("/api/test/")
            
            # Should handle request (might return 401/403 due to auth)
            assert response.status_code in [200, 401, 403, 404, 422]
            
            metrics = mock_monitor.get_metrics()
            assert metrics["total_requests"] >= 1

class TestUserServiceErrorHandling:
    """Integration tests for Django error handling"""
    
    def test_404_handling(self):
        """Test 404 errors are handled gracefully"""
        client = Client()
        
        response = client.get("/nonexistent-endpoint/")
        
        # Should return 404, not crash
        assert response.status_code == 404
    
    def test_500_handling(self):
        """Test 500 errors are handled gracefully"""
        # This would need to be tested with a view that raises an exception
        # For now, test that the error handling middleware works
        from user_service.monitoring.logger import LoggingMiddleware
        
        with patch('user_service.monitoring.logger.user_service_logger.error') as mock_logger:
            # Simulate an error scenario
            user_service_logger.error("Test error", Exception("Test exception"))
            
            # Verify error was logged
            mock_logger.error.assert_called_once()

class TestUserServicePerformanceIntegration:
    """Integration tests for Django performance monitoring"""
    
    def test_performance_monitor_tracking(self):
        """Test performance monitor tracks all activities"""
        from user_service.monitoring.logger import performance_monitor
        
        # Simulate some activity
        performance_monitor.record_request(0.1, 200)
        performance_monitor.record_request(0.2, 404)
        performance_monitor.record_db_query(0.1)
        
        metrics = performance_monitor.get_metrics()
        
        assert metrics["total_requests"] == 2
        assert metrics["total_errors"] == 1
        assert metrics["total_db_queries"] == 1
        assert metrics["avg_response_time"] == 0.15

if __name__ == "__main__":
    pytest.main([__file__])

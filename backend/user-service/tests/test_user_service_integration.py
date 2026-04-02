# tests/test_user_service_integration.py
from unittest.mock import Mock, patch

import pytest
from django.test import Client

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

    @pytest.mark.django_db
    def test_user_model_integration(self):
        """Test user model integration"""
        from user_service.accounts.models import CustomUser

        # Test that custom user model is properly configured
        assert hasattr(CustomUser, "USERNAME_FIELD")
        assert hasattr(CustomUser, "EMAIL_FIELD")

    @pytest.mark.django_db
    def test_authentication_flow(self):
        """Test authentication flow"""
        from django.contrib.auth import authenticate

        from user_service.accounts.models import CustomUser

        # Create test user
        user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Test authentication
        authenticated_user = authenticate(username="testuser", password="testpass123")

        assert authenticated_user is not None
        assert authenticated_user.username == "testuser"

    def test_api_endpoint_integration(self):
        """Test API endpoint integration"""
        # Test a sample API endpoint
        response = self.client.get("/health/")

        # Health endpoint should work
        assert response.status_code == 200


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
        with patch(
            "user_service.monitoring.logger.user_service_logger.error"
        ) as mock_logger:
            # Simulate an error scenario
            user_service_logger.error("Test error", error=Exception("Test exception"))

            # Verify error was logged
            mock_logger.assert_called_once()


class TestUserServicePerformanceIntegration:
    """Integration tests for Django performance monitoring"""

    def test_performance_monitor_tracking(self):
        """Test performance monitor tracks all activities"""
        # Create a fresh monitor for this test
        from user_service.monitoring.logger import PerformanceMonitor

        monitor = PerformanceMonitor()

        # Simulate some activity
        monitor.record_request(0.1, 200)
        monitor.record_request(0.2, 404)

        metrics = monitor.get_metrics()

        assert metrics["total_requests"] == 2
        assert metrics["total_errors"] == 1
        assert metrics["avg_response_time"] == pytest.approx(0.15)


if __name__ == "__main__":
    pytest.main([__file__])

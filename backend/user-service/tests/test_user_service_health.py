# tests/test_user_service_health.py
import time
from unittest.mock import Mock, patch

import pytest
from django.test import Client

from user_service.monitoring.health import (
    detailed_health_check,
    get_metrics,
    health_check,
    test_database_connection,
)


@pytest.mark.django_db
class TestUserServiceHealthEndpoints:
    """Test cases for Django health check endpoints"""

    def setup_method(self):
        """Setup test client"""
        self.client = Client()

    def test_basic_health_check(self):
        """Test basic health check endpoint"""
        response = self.client.get("/health/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["service"] == "maargha-user-service"

    def test_detailed_health_check_success(self):
        """Test detailed health check with all services healthy"""
        with patch(
            "user_service.monitoring.health.test_database_connection"
        ) as mock_db:
            mock_db.return_value = "healthy"

            response = self.client.get("/health/detailed")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["checks"]["database"] == "healthy"
            assert "metrics" in data

    def test_detailed_health_check_degraded(self):
        """Test detailed health check with degraded services"""
        with patch(
            "user_service.monitoring.health.test_database_connection"
        ) as mock_db:
            mock_db.return_value = "unhealthy"

            response = self.client.get("/health/detailed")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "degraded"
            assert data["checks"]["database"] == "unhealthy"

    def test_detailed_health_check_failure(self):
        """Test detailed health check with exception"""
        with patch(
            "user_service.monitoring.health.test_database_connection"
        ) as mock_db:
            mock_db.side_effect = Exception("Database connection failed")

            response = self.client.get("/health/detailed")

            assert response.status_code == 503

    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        with patch(
            "user_service.monitoring.health.performance_monitor"
        ) as mock_monitor:
            mock_monitor.get_metrics.return_value = {
                "total_requests": 100,
                "total_errors": 5,
                "avg_response_time": 0.5,
            }

            response = self.client.get("/health/metrics")

            assert response.status_code == 200
            data = response.json()
            assert data["total_requests"] == 100
            assert data["total_errors"] == 5

    def test_readiness_check_ready(self):
        """Test readiness check when service is ready"""
        with patch(
            "user_service.monitoring.health.performance_monitor"
        ) as mock_monitor:
            mock_monitor.get_metrics.return_value = {
                "total_requests": 50,
                "total_errors": 0,
                "avg_response_time": 0.1,
            }

            response = self.client.get("/health/readiness")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ready"
            assert data["checks"]["has_processed_requests"] is True

    def test_readiness_check_not_ready(self):
        """Test readiness check when service is not ready"""
        with patch(
            "user_service.monitoring.health.performance_monitor"
        ) as mock_monitor:
            mock_monitor.get_metrics.return_value = {
                "total_requests": 0,
                "total_errors": 0,
                "avg_response_time": 0,
            }

            response = self.client.get("/health/readiness")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "not_ready"
            assert data["checks"]["has_processed_requests"] is False

    def test_liveness_check(self):
        """Test liveness check endpoint"""
        response = self.client.get("/health/liveness")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"
        assert "timestamp" in data
        assert data["service"] == "maargha-user-service"


@pytest.mark.django_db
class TestUserServiceHealthCheckFunctions:
    """Test cases for Django health check utility functions"""

    def test_database_connection_success(self):
        """Test successful database connection"""
        with patch("django.db.connection") as mock_connection:
            mock_cursor = Mock()
            mock_connection.cursor.return_value.__enter__ = Mock(
                return_value=mock_cursor
            )
            mock_connection.cursor.return_value.__exit__ = Mock(return_value=False)

            result = test_database_connection()

            assert result == "healthy"

    def test_database_connection_failure(self):
        """Test failed database connection"""
        with patch("django.db.connection") as mock_connection:
            mock_connection.cursor.side_effect = Exception("Connection failed")

            result = test_database_connection()

            assert result == "unhealthy"


if __name__ == "__main__":
    pytest.main([__file__])

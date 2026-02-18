# tests/test_gateway_health.py
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from app.monitoring.health import router, test_external_services

class TestGatewayHealthEndpoints:
    """Test cases for gateway health check endpoints"""
    
    def setup_method(self):
        """Setup test client"""
        from app.main import app
        self.client = TestClient(app)
    
    def test_basic_health_check(self):
        """Test basic health check endpoint"""
        response = self.client.get("/health/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["service"] == "maargha-gateway"
    
    def test_detailed_health_check_success(self):
        """Test detailed health check with all services healthy"""
        with patch('app.monitoring.health.test_external_services') as mock_external:
            mock_external.return_value = asyncio.Future()
            mock_external.return_value.set_result({"orchestrator": "healthy"})
                
            response = self.client.get("/health/detailed")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["checks"]["external_services"]["orchestrator"] == "healthy"
            assert "metrics" in data
    
    def test_detailed_health_check_degraded(self):
        """Test detailed health check with degraded services"""
        with patch('app.monitoring.health.test_external_services') as mock_external:
            mock_external.return_value = asyncio.Future()
            mock_external.return_value.set_result({"orchestrator": "unhealthy"})
            
            response = self.client.get("/health/detailed")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "degraded"
            assert data["checks"]["external_services"]["orchestrator"] == "unhealthy"
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        with patch('app.monitoring.health.performance_monitor') as mock_monitor:
            mock_monitor.get_metrics.return_value = {
                "total_requests": 100,
                "total_errors": 5,
                "active_connections": 10
            }
            
            response = self.client.get("/health/metrics")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_requests"] == 100
            assert data["total_errors"] == 5
            assert data["active_connections"] == 10

@pytest.mark.asyncio
class TestGatewayHealthCheckFunctions:
    """Test cases for gateway health check utility functions"""
    
    async def test_external_services_success(self):
        """Test successful external service checks"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await test_external_services()
            
            assert result["orchestrator"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_external_services_failure(self):
        """Test failed external service checks"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Service unavailable")
            
            with patch('app.monitoring.health.monitoring_logger') as mock_logger:
                result = await test_external_services()
                
                assert result["orchestrator"] == "unhealthy"
                # Verify warning was logged
                mock_logger.warning.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__])

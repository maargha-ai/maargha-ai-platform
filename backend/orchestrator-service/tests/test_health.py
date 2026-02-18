# tests/test_health.py
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from app.monitoring.health import router, test_database_connection, test_external_services

class TestHealthEndpoints:
    """Test cases for health check endpoints"""
    
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
        assert data["service"] == "maargha-orchestrator"
    
    def test_detailed_health_check_success(self):
        """Test detailed health check with all services healthy"""
        with patch('app.monitoring.health.test_database_connection') as mock_db:
            mock_db.return_value = asyncio.Future()
            mock_db.return_value.set_result("healthy")
            
            with patch('app.monitoring.health.test_external_services') as mock_external:
                mock_external.return_value = asyncio.Future()
                mock_external.return_value.set_result({"groq_api": "healthy"})
                
                response = self.client.get("/health/detailed")
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "healthy"
                assert data["checks"]["database"] == "healthy"
                assert data["checks"]["external_services"]["groq_api"] == "healthy"
                assert "metrics" in data
    
    def test_detailed_health_check_degraded(self):
        """Test detailed health check with degraded services"""
        with patch('app.monitoring.health.test_database_connection') as mock_db:
            mock_db.return_value = asyncio.Future()
            mock_db.set_result("unhealthy")
            
            response = self.client.get("/health/detailed")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "degraded"
            assert data["checks"]["database"] == "unhealthy"
    
    def test_detailed_health_check_failure(self):
        """Test detailed health check with exception"""
        with patch('app.monitoring.health.test_database_connection') as mock_db:
            mock_db.side_effect = Exception("Database connection failed")
            
            response = self.client.get("/health/detailed")
            
            assert response.status_code == 503
    
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
    
    def test_readiness_check_ready(self):
        """Test readiness check when service is ready"""
        with patch('app.monitoring.health.performance_monitor') as mock_monitor:
            mock_monitor.get_metrics.return_value = {
                "total_requests": 50,
                "active_connections": 5
            }
            
            response = self.client.get("/health/readiness")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ready"
            assert data["checks"]["has_processed_requests"] is True
            assert data["checks"]["active_connections"] == 5
    
    def test_readiness_check_not_ready(self):
        """Test readiness check when service is not ready"""
        with patch('app.monitoring.health.performance_monitor') as mock_monitor:
            mock_monitor.get_metrics.return_value = {
                "total_requests": 0,
                "active_connections": 0
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
        assert data["service"] == "maargha-orchestrator"

class TestHealthCheckFunctions:
    """Test cases for health check utility functions"""
    
    @pytest.mark.asyncio
    async def test_database_connection_success(self):
        """Test successful database connection"""
        with patch('app.monitoring.health.engine') as mock_engine:
            mock_conn = AsyncMock()
            mock_engine.begin.return_value.__aenter__.return_value = mock_conn
            
            result = await test_database_connection()
            
            assert result == "healthy"
            mock_conn.execute.assert_called_with("SELECT 1")
    
    @pytest.mark.asyncio
    async def test_database_connection_failure(self):
        """Test failed database connection"""
        with patch('app.monitoring.health.engine') as mock_engine:
            mock_engine.begin.side_effect = Exception("Connection failed")
            
            result = await test_database_connection()
            
            assert result == "unhealthy"
    
    @pytest.mark.asyncio
    async def test_external_services_success(self):
        """Test successful external service checks"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await test_external_services()
            
            assert result["groq_api"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_external_services_failure(self):
        """Test failed external service checks"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Service unavailable")
            
            with patch('app.monitoring.health.monitoring_logger') as mock_logger:
                result = await test_external_services()
                
                assert result["groq_api"] == "unhealthy"
                # Verify warning was logged
                mock_logger.warning.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__])

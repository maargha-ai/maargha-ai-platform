# tests/conftest.py
import asyncio
import os
from unittest.mock import AsyncMock, patch

import pytest

os.environ.setdefault("USER_SERVICE_URL", "http://localhost:8000")
os.environ.setdefault("LLM_PROVIDER", "groq")
os.environ.setdefault("OPENAI_API_KEY", "dummy")
os.environ.setdefault("GROQ_API_KEY", "dummy")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db",
)
os.environ.setdefault("SONG_PATH", "dummy")


@pytest.fixture
def mock_websocket():
    """Create a mock WebSocket for testing"""
    websocket = AsyncMock()
    websocket.accept.return_value = None
    websocket.receive_text.return_value = "test message"
    websocket.send_text.return_value = None
    return websocket


@pytest.fixture
def mock_performance_monitor():
    """Create a mock performance monitor"""
    with patch("app.monitoring.logger.performance_monitor") as mock:
        mock.get_metrics.return_value = {
            "total_requests": 0,
            "total_errors": 0,
            "total_websocket_connections": 0,
            "active_connections": 0,
            "avg_response_time": 0,
            "max_response_time": 0,
            "min_response_time": 0,
            "error_rate": 0,
        }
        yield mock


@pytest.fixture
def mock_logger():
    """Create a mock logger"""
    with patch("app.monitoring.logger.orchestrator_logger") as mock:
        yield mock


@pytest.fixture
def sample_graph_response():
    """Sample graph response for testing"""
    return {
        "agent_response": "This is a test response from the AI agent.",
        "messages": [
            {"role": "user", "content": "test input"},
            {
                "role": "assistant",
                "content": "This is a test response from the AI agent.",
            },
        ],
    }


@pytest.fixture
def sample_navigation_response():
    """Sample navigation response for testing"""
    return {
        "navigate": "/roadmap",
        "messages": [
            {"role": "user", "content": "take me to roadmap"},
            {"role": "assistant", "content": "Navigating to roadmap..."},
        ],
    }

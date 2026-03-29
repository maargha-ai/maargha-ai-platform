# tests/test_websocket.py
import asyncio
import json
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import WebSocket
from fastapi.testclient import TestClient


class TestWebSocketHandlers:
    """Test cases for WebSocket handlers"""

    def setup_method(self):
        """Setup test client with mocked dependencies"""
        with patch('app.utils.gcs.get_storage_client') as mock_gcs:
            mock_gcs.return_value = Mock()
            from app.main import app
            self.client = TestClient(app)

    @pytest.mark.asyncio
    async def test_chat_websocket_connection(self):
        """Test chat WebSocket connection and message handling"""
        with patch("app.main.performance_monitor") as mock_monitor:
            with patch("app.main.orchestrator_logger") as mock_logger:
                with patch("app.main.graph_app") as mock_graph:

                    # Mock graph response
                    mock_graph.ainvoke.return_value = {
                        "agent_response": "Test response"
                    }

                    # Create WebSocket mock
                    mock_websocket = AsyncMock(spec=WebSocket)
                    mock_websocket.accept.return_value = None
                    mock_websocket.receive_text.return_value = "Hello"
                    mock_websocket.send_text.return_value = None

                    # Import and test the function
                    from app.main import chat_ws

                    await chat_ws(mock_websocket)

                    # Verify connection was recorded
                    mock_monitor.record_websocket_connection.assert_called_once()

                    # Verify message was logged
                    mock_logger.info.assert_called()

                    # Verify response was sent
                    expected_response = {"type": "CHAT", "content": "Test response"}
                    mock_websocket.send_text.assert_called_with(
                        json.dumps(expected_response)
                    )

    @pytest.mark.asyncio
    async def test_chat_websocket_navigation(self):
        """Test chat WebSocket with navigation command"""
        with patch("app.main.performance_monitor") as mock_monitor:
            with patch("app.main.orchestrator_logger") as mock_logger:
                with patch("app.main.graph_app") as mock_graph:

                    # Mock graph response with navigation
                    mock_graph.ainvoke.return_value = {"navigate": "/roadmap"}

                    mock_websocket = AsyncMock(spec=WebSocket)
                    mock_websocket.accept.return_value = None
                    mock_websocket.receive_text.return_value = "Navigate me"
                    mock_websocket.send_text.return_value = None

                    from app.main import chat_ws

                    await chat_ws(mock_websocket)

                    # Verify navigation command was sent
                    expected_navigation = {"navigate": "/roadmap"}
                    mock_websocket.send_text.assert_any_call(
                        json.dumps(expected_navigation)
                    )

    @pytest.mark.asyncio
    async def test_chat_websocket_disconnect(self):
        """Test chat WebSocket disconnection handling"""
        with patch("app.main.performance_monitor") as mock_monitor:
            with patch("app.main.orchestrator_logger") as mock_logger:
                with patch("app.main.graph_app") as mock_graph:

                    # Mock graph response
                    mock_graph.ainvoke.return_value = {
                        "agent_response": "Test response"
                    }

                    mock_websocket = AsyncMock(spec=WebSocket)
                    mock_websocket.accept.return_value = None
                    mock_websocket.receive_text.side_effect = [
                        "Hello",
                        Exception("Disconnect"),
                    ]
                    mock_websocket.send_text.return_value = None

                    from app.main import chat_ws

                    with pytest.raises(Exception):
                        await chat_ws(mock_websocket)

                    # Verify disconnection was recorded
                    mock_monitor.record_websocket_disconnection.assert_called_once()

                    # Verify disconnection was logged
                    mock_logger.info.assert_any_call()


class TestWebSocketErrorHandling:
    """Test cases for WebSocket error handling"""

    @pytest.mark.asyncio
    async def test_websocket_error_logging(self):
        """Test WebSocket errors are properly logged"""
        with patch("app.main.performance_monitor") as mock_monitor:
            with patch("app.main.orchestrator_logger") as mock_logger:
                with patch("app.main.graph_app") as mock_graph:

                    # Mock graph to raise exception
                    mock_graph.ainvoke.side_effect = Exception("Graph error")

                    mock_websocket = AsyncMock(spec=WebSocket)
                    mock_websocket.accept.return_value = None
                    mock_websocket.receive_text.return_value = "Test message"

                    from app.main import chat_ws

                    with pytest.raises(Exception):
                        await chat_ws(mock_websocket)

                    # Verify error was logged
                    mock_logger.error.assert_called_once()
                    error_call = mock_logger.error.call_args
                    assert "Chat WebSocket error" in error_call[0][0]
                    assert error_call[1]["error"] is not None


class TestWebSocketMessageProcessing:
    """Test cases for WebSocket message processing"""

    @pytest.mark.asyncio
    async def test_message_state_management(self):
        """Test message state is properly managed"""
        with patch("app.main.performance_monitor") as mock_monitor:
            with patch("app.main.orchestrator_logger") as mock_logger:
                with patch("app.main.graph_app") as mock_graph:

                    # Mock graph responses
                    mock_graph.ainvoke.side_effect = [
                        {"agent_response": "First response"},
                        {"agent_response": "Second response"},
                    ]

                    mock_websocket = AsyncMock(spec=WebSocket)
                    mock_websocket.accept.return_value = None
                    mock_websocket.receive_text.side_effect = [
                        "Message 1",
                        "Message 2",
                        Exception("Done"),
                    ]
                    mock_websocket.send_text.return_value = None

                    from app.main import chat_ws

                    with pytest.raises(Exception):
                        await chat_ws(mock_websocket)

                    # Verify state is maintained across messages
                    assert mock_graph.ainvoke.call_count == 2

                    # Verify both responses were sent
                    assert mock_websocket.send_text.call_count == 2

                    # Verify message logging
                    assert (
                        mock_logger.info.call_count >= 4
                    )  # Connection + 2 messages + 2 responses


if __name__ == "__main__":
    pytest.main([__file__])

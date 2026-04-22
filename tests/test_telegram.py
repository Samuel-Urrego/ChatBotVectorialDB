import sys
import os
from unittest.mock import MagicMock, AsyncMock, patch

# Set dummy environment variables for testing
os.environ["OPENAI_API_KEY"] = "fake"
os.environ["PINECONE_API_KEY"] = "fake"
os.environ["PINECONE_INDEX_NAME"] = "fake"
os.environ["DATABASE_URL"] = "sqlite:///test.db"
os.environ["TELEGRAM_TOKEN"] = "123456789:ABCDEFGH"

# Mock problematic modules before importing app
mock_mod = MagicMock()
sys.modules["pinecone"] = mock_mod
sys.modules["langchain"] = mock_mod
sys.modules["langchain_pinecone"] = mock_mod
sys.modules["langchain_openai"] = mock_mod
sys.modules["langchain_community"] = mock_mod
sys.modules["langchain_classic"] = mock_mod
sys.modules["langchain_classic.chains"] = mock_mod
sys.modules["langchain_core"] = mock_mod
sys.modules["langchain_core.prompts"] = mock_mod

from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

@patch("app.main.Update")
@patch("app.main.chat_service")
@patch("app.main.bot")
def test_telegram_webhook_success(mock_bot, mock_chat_service, mock_update_class):
    """
    Test that the webhook correctly handles a message and calls the chat service.
    """
    # Setup mocks
    mock_chat_service.get_answer_with_sources.return_value = {
        "answer": "Esta es una respuesta de prueba.",
        "sources": ["test.pdf"]
    }
    
    # Mock the Update object
    mock_update = MagicMock()
    mock_update.message.chat_id = 12345
    mock_update.message.text = "¿Cómo funciona el sistema?"
    mock_update_class.de_json.return_value = mock_update
    
    # Mock the async context manager for the bot
    mock_bot.__aenter__ = AsyncMock(return_value=mock_bot)
    mock_bot.__aexit__ = AsyncMock(return_value=None)
    mock_bot.send_message = AsyncMock()
    
    # Sample Telegram update (payload doesn't matter much now since we mock de_json)
    payload = {"update_id": 1}
    
    response = client.post("/telegram-webhook", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
    # Verify interaction
    mock_chat_service.get_answer_with_sources.assert_called_once_with("¿Cómo funciona el sistema?")
    
    # Verify message sent back
    expected_text = "Esta es una respuesta de prueba.\n\nFuentes:\n- test.pdf\n"
    mock_bot.send_message.assert_called_once()
    args, kwargs = mock_bot.send_message.call_args
    assert kwargs["chat_id"] == 12345
    assert kwargs["text"] == expected_text

import pytest
import os
from unittest.mock import MagicMock
from clients.GroqClient import GroqClient

@pytest.fixture
def mock_groq_client(mocker):
    return mocker.patch('clients.GroqClient.Groq')

def test_init_with_key(mock_groq_client):
    client = GroqClient(api_key="test_key")
    assert client.api_key == "test_key"
    mock_groq_client.assert_called_once_with(api_key="test_key")

def test_init_without_key(mocker):
    # Ensure env var is not set
    mocker.patch.dict(os.environ, {}, clear=True)
    with pytest.raises(ValueError, match="A chave da API da Groq é obrigatória"):
        GroqClient()

def test_init_with_env_key(mocker, mock_groq_client):
    mocker.patch.dict(os.environ, {"GROQ_API_KEY": "env_key"}, clear=True)
    client = GroqClient()
    assert client.api_key == "env_key"
    mock_groq_client.assert_called_once_with(api_key="env_key")

def test_invoke_success(mock_groq_client):
    # Setup mock
    mock_instance = mock_groq_client.return_value
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content="Hello there!"))
    ]
    mock_instance.chat.completions.create.return_value = mock_completion

    client = GroqClient(api_key="test_key")
    result = client.invoke("Hi")

    assert result == "Hello there!"
    mock_instance.chat.completions.create.assert_called_once()
    
    # Verify arguments
    call_args = mock_instance.chat.completions.create.call_args
    assert call_args.kwargs['messages'][0]['content'] == "Hi"
    # Verify default model
    assert call_args.kwargs['model'] == "llama-3.3-70b-versatile"

def test_invoke_custom_model(mock_groq_client):
    # Setup mock
    mock_instance = mock_groq_client.return_value
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content="Hello"))
    ]
    mock_instance.chat.completions.create.return_value = mock_completion

    client = GroqClient(api_key="test_key")
    client.invoke("Hi", model="custom-model")
    
    call_args = mock_instance.chat.completions.create.call_args
    assert call_args.kwargs['model'] == "custom-model"

def test_invoke_api_error(mock_groq_client):
    # Setup mock to raise exception
    mock_instance = mock_groq_client.return_value
    mock_instance.chat.completions.create.side_effect = Exception("API Error")

    client = GroqClient(api_key="test_key")

    with pytest.raises(Exception, match="API Error"):
        client.invoke("Hi")
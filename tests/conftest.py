"""
Pytest configuration and fixtures for all tests
"""
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_database():
    """Mock database for testing"""
    with patch('backend.database.Database') as mock_db:
        mock_db.connect = MagicMock()
        mock_db.query = MagicMock()
        mock_db.insert = MagicMock()
        mock_db.update = MagicMock()
        mock_db.delete = MagicMock()
        yield mock_db


@pytest.fixture
def mock_audio_file():
    """Mock audio file for testing"""
    mock_file = MagicMock()
    mock_file.name = "test_audio.wav"
    mock_file.size = 1024000  # 1MB
    mock_file.format = "wav"
    mock_file.read = MagicMock(return_value=b"audio_data")
    return mock_file


@pytest.fixture
def mock_user_session():
    """Mock user session"""
    session = {
        "user_id": "test_user_123",
        "session_id": "session_456",
        "timestamp": "2024-01-01T00:00:00Z",
        "is_active": True,
        "language": "en-US"
    }
    return session


@pytest.fixture
def mock_conversation():
    """Mock conversation data"""
    return {
        "conversation_id": "conv_123",
        "user_id": "user_123",
        "messages": [
            {
                "role": "user",
                "content": "Hello, how are you?",
                "timestamp": "2024-01-01T00:00:00Z"
            },
            {
                "role": "assistant",
                "content": "I'm doing well, thank you for asking!",
                "timestamp": "2024-01-01T00:00:01Z"
            }
        ],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:01Z"
    }


@pytest.fixture
def mock_api_key():
    """Mock API key for testing"""
    return "test_api_key_123456789"


@pytest.fixture
def mock_config():
    """Mock configuration"""
    config = {
        "debug": True,
        "database_url": "sqlite:///:memory:",
        "api_timeout": 30,
        "max_file_size": 50 * 1024 * 1024,  # 50MB
        "supported_formats": ["wav", "mp3", "flac", "ogg"],
        "max_history_size": 1000,
        "log_level": "DEBUG"
    }
    return config


@pytest.fixture
def temp_audio_file(tmp_path):
    """Create a temporary audio file for testing"""
    audio_file = tmp_path / "test_audio.wav"
    audio_file.write_bytes(b"RIFF" + b"\x00" * 100)  # Minimal WAV header
    return audio_file


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file"""
    import json
    config_file = tmp_path / "config.json"
    config = {
        "debug": True,
        "database_url": "sqlite:///:memory:"
    }
    config_file.write_text(json.dumps(config))
    return config_file


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_logger():
    """Mock logger for testing"""
    with patch('backend.logger.Logger') as mock_log:
        mock_log.debug = MagicMock()
        mock_log.info = MagicMock()
        mock_log.warning = MagicMock()
        mock_log.error = MagicMock()
        mock_log.critical = MagicMock()
        yield mock_log


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "e2e: marks tests as end-to-end tests")
    config.addinivalue_line("markers", "external: marks tests that require external services")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add markers based on test location
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        if "e2e" in item.nodeid or "end_to_end" in item.nodeid:
            item.add_marker(pytest.mark.e2e)


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks after each test"""
    yield
    # Cleanup after test


@pytest.fixture
def cli_runner():
    """CLI test runner"""
    from click.testing import CliRunner
    return CliRunner()


@pytest.fixture
def http_client():
    """Mock HTTP client for API testing"""
    from unittest.mock import MagicMock
    client = MagicMock()
    client.get = MagicMock()
    client.post = MagicMock()
    client.put = MagicMock()
    client.delete = MagicMock()
    client.patch = MagicMock()
    return client

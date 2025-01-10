"""Test configuration and fixtures."""

from typing import Any, Dict

import pytest

from hunter_sdk import HunterClient, HunterConfig
from hunter_sdk.storage import MemoryStorage


@pytest.fixture
def hunter_config() -> HunterConfig:
    """Create test configuration."""
    return HunterConfig(api_key='test-api-key')


@pytest.fixture
def memory_storage() -> MemoryStorage:
    """Create clean memory storage instance."""
    return MemoryStorage()


@pytest.fixture
def mock_email_verification_response() -> Dict[str, Any]:
    """Create mock email verification response."""
    return {
        'status': 'valid',
        'score': 95,
        'email': 'test@example.com',
        'domain': 'example.com',
        'sources': [],
    }


@pytest.fixture
def hunter_client(mocker, hunter_config, mock_email_verification_response) -> HunterClient:
    """Create mock Hunter client."""
    client = HunterClient(hunter_config)
    mocker.patch.object(
        client._session,
        'get',
        return_value=mocker.Mock(
            ok=True,
            json=lambda: {'data': mock_email_verification_response},
        ),
    )
    return client 
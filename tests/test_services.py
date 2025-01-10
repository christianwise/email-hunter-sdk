"""Tests for service layer implementations."""

from typing import Any, Dict

import pytest

from hunter_sdk import HunterClient
from hunter_sdk.services import EmailVerificationService
from hunter_sdk.storage import MemoryStorage


def test_verify_email_first_call(
    hunter_client: HunterClient,
    memory_storage: MemoryStorage,
    mock_email_verification_response: Dict[str, Any],
) -> None:
    """Test first email verification call uses API."""
    service = EmailVerificationService(hunter_client, memory_storage)
    result = service.verify_email('test@example.com')
    
    assert result == mock_email_verification_response
    assert memory_storage.read('test@example.com') == mock_email_verification_response


def test_verify_email_cached(
    hunter_client: HunterClient,
    memory_storage: MemoryStorage,
    mock_email_verification_response: Dict[str, Any],
    mocker,
) -> None:
    """Test subsequent email verification calls use cache."""
    service = EmailVerificationService(hunter_client, memory_storage)
    memory_storage.create('test@example.com', mock_email_verification_response)
    
    # Mock the client to ensure it's not called
    mock_verify = mocker.patch.object(hunter_client, 'verify_email')
    
    result = service.verify_email('test@example.com')
    
    assert result == mock_email_verification_response
    mock_verify.assert_not_called()


def test_verify_email_force_refresh(
    hunter_client: HunterClient,
    memory_storage: MemoryStorage,
    mock_email_verification_response: Dict[str, Any],
) -> None:
    """Test force refresh bypasses cache."""
    service = EmailVerificationService(hunter_client, memory_storage)
    memory_storage.create('test@example.com', {'old': 'data'})
    
    result = service.verify_email('test@example.com', force_refresh=True)
    
    assert result == mock_email_verification_response
    assert memory_storage.read('test@example.com') == mock_email_verification_response


def test_clear_cache(
    hunter_client: HunterClient,
    memory_storage: MemoryStorage,
) -> None:
    """Test clearing cache for specific email."""
    service = EmailVerificationService(hunter_client, memory_storage)
    memory_storage.create('test@example.com', {'data': 'test'})
    
    service.clear_cache('test@example.com')
    
    assert memory_storage.read('test@example.com') is None


def test_clear_cache_nonexistent(
    hunter_client: HunterClient,
    memory_storage: MemoryStorage,
) -> None:
    """Test clearing cache for nonexistent email doesn't raise error."""
    service = EmailVerificationService(hunter_client, memory_storage)
    service.clear_cache('nonexistent@example.com')  # Should not raise 
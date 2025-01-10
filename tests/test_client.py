"""Tests for Hunter API client."""

from typing import Any, Dict

import pytest
import requests

from hunter_sdk import HunterClient, HunterConfig
from hunter_sdk.exceptions import ConfigurationError, HunterAPIError


def test_client_init_without_api_key() -> None:
    """Test client initialization without API key raises error."""
    config = HunterConfig(api_key='')
    with pytest.raises(ConfigurationError):
        HunterClient(config)


def test_verify_email_success(
    hunter_client: HunterClient,
    mock_email_verification_response: Dict[str, Any],
) -> None:
    """Test successful email verification."""
    result = hunter_client.verify_email('test@example.com')
    assert result == mock_email_verification_response


def test_verify_email_api_error(hunter_client: HunterClient, mocker) -> None:
    """Test handling of API errors in email verification."""
    error_response = {'errors': [{'details': 'API Error'}]}
    mocker.patch.object(
        hunter_client._session,
        'get',
        return_value=mocker.Mock(
            ok=False,
            status_code=400,
            json=lambda: error_response,
        ),
    )

    with pytest.raises(HunterAPIError) as exc_info:
        hunter_client.verify_email('test@example.com')
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == 'API Error'


def test_verify_email_network_error(hunter_client: HunterClient, mocker) -> None:
    """Test handling of network errors in email verification."""
    mocker.patch.object(
        hunter_client._session,
        'get',
        side_effect=requests.RequestException('Network Error'),
    )

    with pytest.raises(requests.RequestException):
        hunter_client.verify_email('test@example.com') 
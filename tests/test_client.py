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


def test_rate_limiting(hunter_client: HunterClient, mocker) -> None:
    """Test rate limiting in client requests."""
    start_time = time.time()
    
    # Make multiple requests
    for _ in range(3):
        hunter_client.verify_email('test@example.com')
    
    duration = time.time() - start_time
    # With rate limit of 2 per second, this should take at least 1 second
    assert duration >= 1.0


def test_retry_on_server_error(hunter_client: HunterClient, mocker) -> None:
    """Test retry behavior on server errors."""
    responses = [
        mocker.Mock(ok=False, status_code=500),
        mocker.Mock(ok=False, status_code=500),
        mocker.Mock(
            ok=True,
            json=lambda: {'data': {'status': 'valid'}},
        ),
    ]
    
    mock_request = mocker.patch.object(
        hunter_client._session,
        'request',
        side_effect=responses,
    )
    
    result = hunter_client._make_request('GET', 'test')
    
    assert result == {'status': 'valid'}
    assert mock_request.call_count == 3


def test_no_retry_on_client_error(hunter_client: HunterClient, mocker) -> None:
    """Test that client errors are not retried."""
    mock_response = mocker.Mock(
        ok=False,
        status_code=400,
        json=lambda: {'errors': [{'details': 'Bad Request'}]},
    )
    
    mocker.patch.object(
        hunter_client._session,
        'request',
        return_value=mock_response,
    )
    
    with pytest.raises(HunterAPIError) as exc_info:
        hunter_client._make_request('GET', 'test')
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == 'Bad Request'


def test_retry_on_rate_limit(hunter_client: HunterClient, mocker) -> None:
    """Test retry behavior on rate limit errors."""
    responses = [
        mocker.Mock(ok=False, status_code=429),
        mocker.Mock(
            ok=True,
            json=lambda: {'data': {'status': 'valid'}},
        ),
    ]
    
    mock_request = mocker.patch.object(
        hunter_client._session,
        'request',
        side_effect=responses,
    )
    
    result = hunter_client._make_request('GET', 'test')
    
    assert result == {'status': 'valid'}
    assert mock_request.call_count == 2 
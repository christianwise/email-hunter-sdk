"""Tests for domain search service."""

from typing import Any, Dict

import pytest

from hunter_sdk import HunterClient
from hunter_sdk.services import DomainSearchService
from hunter_sdk.storage import MemoryStorage


@pytest.fixture
def mock_domain_search_response() -> Dict[str, Any]:
    """Create mock domain search response."""
    return {
        'domain': 'example.com',
        'emails': [
            {'value': 'test1@example.com', 'type': 'personal'},
            {'value': 'test2@example.com', 'type': 'generic'},
        ],
        'pattern': '{first}@example.com',
    }


@pytest.fixture
def domain_search_service(
    hunter_client: HunterClient,
    memory_storage: MemoryStorage,
    mock_domain_search_response: Dict[str, Any],
    mocker,
) -> DomainSearchService:
    """Create domain search service with mocked client."""
    mocker.patch.object(
        hunter_client,
        'domain_search',
        return_value=mock_domain_search_response,
    )
    return DomainSearchService(hunter_client, memory_storage)


def test_search_domain_first_call(
    domain_search_service: DomainSearchService,
    mock_domain_search_response: Dict[str, Any],
    hunter_client: HunterClient,
) -> None:
    """Test first domain search call uses API."""
    result = domain_search_service.search_domain('example.com')
    assert result == mock_domain_search_response
    hunter_client.domain_search.assert_called_once_with(domain='example.com', type=None)


def test_search_domain_cached(
    domain_search_service: DomainSearchService,
    mock_domain_search_response: Dict[str, Any],
    hunter_client: HunterClient,
    memory_storage: MemoryStorage,
) -> None:
    """Test subsequent domain search calls use cache."""
    memory_storage.create('domain:example.com', mock_domain_search_response)
    
    result = domain_search_service.search_domain('example.com')
    
    assert result == mock_domain_search_response
    hunter_client.domain_search.assert_not_called()


def test_search_domain_force_refresh(
    domain_search_service: DomainSearchService,
    mock_domain_search_response: Dict[str, Any],
    hunter_client: HunterClient,
    memory_storage: MemoryStorage,
) -> None:
    """Test force refresh bypasses cache."""
    old_data = {'domain': 'example.com', 'emails': []}
    memory_storage.create('domain:example.com', old_data)
    
    result = domain_search_service.search_domain('example.com', force_refresh=True)
    
    assert result == mock_domain_search_response
    hunter_client.domain_search.assert_called_once()


def test_iter_all_results(
    domain_search_service: DomainSearchService,
    hunter_client: HunterClient,
    mocker,
) -> None:
    """Test iteration through paginated results."""
    # Mock responses for pagination
    responses = [
        {
            'emails': [{'value': f'test{i}@example.com'} for i in range(2)],
            'domain': 'example.com',
        },
        {
            'emails': [{'value': 'last@example.com'}],
            'domain': 'example.com',
        },
    ]
    
    mock_search = mocker.patch.object(
        hunter_client,
        'domain_search',
        side_effect=responses,
    )
    
    results = list(domain_search_service.iter_all_results('example.com', batch_size=2))
    
    assert len(results) == 2
    assert results == responses
    assert mock_search.call_count == 2
    
    # Verify pagination parameters
    mock_search.assert_has_calls([
        mocker.call(domain='example.com', type=None, limit=2, offset=0),
        mocker.call(domain='example.com', type=None, limit=2, offset=2),
    ]) 
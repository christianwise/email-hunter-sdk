"""Domain search service implementation."""

from typing import Any, Dict, Iterator, Optional

from ..client import HunterClient
from ..storage.base import BaseStorage


class DomainSearchService:
    """Service for domain search with caching."""

    def __init__(self, client: HunterClient, storage: BaseStorage) -> None:
        """Initialize domain search service.

        Args:
            client: Hunter API client instance
            storage: Storage implementation for caching results
        """
        self._client = client
        self._storage = storage

    def search_domain(
        self,
        domain: str,
        force_refresh: bool = False,
        type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for email addresses in a domain with caching.

        Args:
            domain: Domain to search
            force_refresh: If True, bypass cache and fetch fresh data
            type: Type of emails to return (generic or personal)

        Returns:
            Dict containing search results
        """
        cache_key = f"domain:{domain}"
        if type:
            cache_key += f":type:{type}"

        if not force_refresh:
            cached_result = self._storage.read(cache_key)
            if cached_result is not None:
                return cached_result

        result = self._client.domain_search(domain=domain, type=type)
        self._storage.create(cache_key, result)
        return result

    def iter_all_results(
        self,
        domain: str,
        type: Optional[str] = None,
        batch_size: int = 100,
    ) -> Iterator[Dict[str, Any]]:
        """Iterate through all results for a domain search.

        Args:
            domain: Domain to search
            type: Type of emails to return (generic or personal)
            batch_size: Number of results to fetch per request

        Yields:
            Search result batches
        """
        offset = 0
        while True:
            result = self._client.domain_search(
                domain=domain,
                type=type,
                limit=batch_size,
                offset=offset,
            )
            yield result

            if len(result['emails']) < batch_size:
                break

            offset += batch_size 
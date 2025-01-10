"""Hunter API client implementation."""

import time
from typing import Any, Dict, Optional

import requests

from .config import HunterConfig
from .exceptions import ConfigurationError, HunterAPIError
from .utils.rate_limiter import RateLimiter


class HunterClient:
    """Client for interacting with Hunter API."""

    def __init__(self, config: HunterConfig) -> None:
        """Initialize Hunter client.

        Args:
            config: Hunter API configuration

        Raises:
            ConfigurationError: If API key is not provided
        """
        if not config.api_key:
            raise ConfigurationError("API key is required")
        self._config = config
        self._session = requests.Session()
        self._rate_limiter = (
            RateLimiter(config.rate_limit) if config.rate_limit else None
        )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic and rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request parameters

        Returns:
            API response data

        Raises:
            HunterAPIError: If API request fails
        """
        if self._rate_limiter:
            self._rate_limiter.acquire()

        retries = 0
        while True:
            try:
                response = self._session.request(
                    method=method,
                    url=f'{self._config.base_url}/{endpoint}',
                    timeout=self._config.timeout,
                    **kwargs,
                )

                if response.ok:
                    return response.json()['data']

                # Don't retry client errors except 429 (rate limit)
                if 400 <= response.status_code < 500 and response.status_code != 429:
                    raise HunterAPIError(
                        status_code=response.status_code,
                        message=response.json().get('errors', [{'details': 'Unknown error'}])[0]['details'],
                    )

                retries += 1
                if retries >= self._config.max_retries:
                    raise HunterAPIError(
                        status_code=response.status_code,
                        message=f"Max retries ({self._config.max_retries}) exceeded",
                    )

                # Exponential backoff
                time.sleep(self._config.retry_delay * (2 ** (retries - 1)))

            except requests.RequestException as e:
                retries += 1
                if retries >= self._config.max_retries:
                    raise

                time.sleep(self._config.retry_delay * (2 ** (retries - 1)))

    def verify_email(self, email: str) -> Dict[str, Any]:
        """Verify email address using Hunter API.

        Args:
            email: Email address to verify

        Returns:
            Dict containing verification results

        Raises:
            HunterAPIError: If API request fails
        """
        return self._make_request(
            'GET',
            'email-verifier',
            params={'email': email, 'api_key': self._config.api_key},
        )

    def domain_search(
        self,
        domain: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for email addresses in a domain.

        Args:
            domain: Domain to search
            limit: Maximum number of results per page
            offset: Number of results to skip
            type: Type of emails to return (generic or personal)

        Returns:
            Dict containing search results

        Raises:
            HunterAPIError: If API request fails
        """
        params = {
            'domain': domain,
            'api_key': self._config.api_key,
        }
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if type is not None:
            params['type'] = type

        return self._make_request('GET', 'domain-search', params=params) 
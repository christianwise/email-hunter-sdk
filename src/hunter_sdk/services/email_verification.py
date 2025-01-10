"""Email verification service implementation."""

from typing import Any, Dict, Optional

from ..client import HunterClient
from ..storage.base import BaseStorage


class EmailVerificationService:
    """Service for email verification with caching."""

    def __init__(self, client: HunterClient, storage: BaseStorage) -> None:
        """Initialize email verification service.

        Args:
            client: Hunter API client instance
            storage: Storage implementation for caching results
        """
        self._client = client
        self._storage = storage

    def verify_email(self, email: str, force_refresh: bool = False) -> Dict[str, Any]:
        """Verify email address with caching.

        Args:
            email: Email address to verify
            force_refresh: If True, bypass cache and fetch fresh data

        Returns:
            Dict containing verification results
        """
        if not force_refresh:
            cached_result = self._storage.read(email)
            if cached_result is not None:
                return cached_result

        result = self._client.verify_email(email)
        self._storage.create(email, result)
        return result

    def get_cached_result(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached verification result.

        Args:
            email: Email address to look up

        Returns:
            Cached verification result or None if not found
        """
        return self._storage.read(email)

    def clear_cache(self, email: str) -> None:
        """Clear cached verification result for an email.

        Args:
            email: Email address to clear from cache
        """
        try:
            self._storage.delete(email)
        except KeyError:
            pass  # Ignore if email not in cache 
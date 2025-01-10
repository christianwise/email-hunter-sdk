from typing import Any, Dict, Optional

from .base import BaseStorage


class MemoryStorage(BaseStorage):
    """In-memory implementation of storage using a dictionary."""

    def __init__(self) -> None:
        """Initialize empty storage."""
        self._storage: Dict[str, Dict[str, Any]] = {}

    def create(self, key: str, value: Dict[str, Any]) -> None:
        """Create a new record in storage.

        Args:
            key: Unique identifier for the record
            value: Data to store

        Raises:
            KeyError: If key already exists in storage
        """
        if key in self._storage:
            raise KeyError(f"Key '{key}' already exists in storage")
        self._storage[key] = value.copy()

    def read(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a record from storage.

        Args:
            key: Unique identifier for the record

        Returns:
            The stored data or None if not found
        """
        return self._storage.get(key)

    def update(self, key: str, value: Dict[str, Any]) -> None:
        """Update an existing record in storage.

        Args:
            key: Unique identifier for the record
            value: New data to store

        Raises:
            KeyError: If key doesn't exist in storage
        """
        if key not in self._storage:
            raise KeyError(f"Key '{key}' not found in storage")
        self._storage[key] = value.copy()

    def delete(self, key: str) -> None:
        """Delete a record from storage.

        Args:
            key: Unique identifier for the record

        Raises:
            KeyError: If key doesn't exist in storage
        """
        if key not in self._storage:
            raise KeyError(f"Key '{key}' not found in storage")
        del self._storage[key] 
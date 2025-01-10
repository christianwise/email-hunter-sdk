from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseStorage(ABC):
    """Abstract base class for storage implementations."""

    @abstractmethod
    def create(self, key: str, value: Dict[str, Any]) -> None:
        """Create a new record in storage.

        Args:
            key: Unique identifier for the record
            value: Data to store
        """
        pass

    @abstractmethod
    def read(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a record from storage.

        Args:
            key: Unique identifier for the record

        Returns:
            The stored data or None if not found
        """
        pass

    @abstractmethod
    def update(self, key: str, value: Dict[str, Any]) -> None:
        """Update an existing record in storage.

        Args:
            key: Unique identifier for the record
            value: New data to store
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a record from storage.

        Args:
            key: Unique identifier for the record
        """
        pass 
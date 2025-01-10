# Hunter.io Python SDK

A Python SDK for interacting with the Hunter.io API, featuring caching, rate limiting, and retry mechanisms.

## Features

- Email verification endpoint support
- Domain search with pagination
- In-memory caching of API responses
- Rate limiting to respect API quotas
- Automatic retries with exponential backoff
- Thread-safe implementation
- Comprehensive type hints
- Extensive test coverage

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from hunter_sdk import HunterClient, HunterConfig
from hunter_sdk.storage import MemoryStorage

#Initialize components
config = HunterConfig(
    api_key='your-api-key-here',
    rate_limit=100, # Optional: limit requests per minute
)
client = HunterClient(config)
storage = MemoryStorage()

# Verify email
result = client.verify_email('test@example.com')
print(result)

# Store result in cache
storage.create('test@example.com', result)

# Retrieve from cache
cached_result = storage.read('test@example.com')
print(cached_result)
```

## Configuration

The `HunterConfig` class supports the following options:

- `api_key`: Your Hunter.io API key (required)
- `base_url`: API base URL (default: 'https://api.hunter.io/v2')
- `timeout`: Request timeout in seconds (default: 30)
- `max_retries`: Maximum number of retry attempts (default: 3)
- `retry_delay`: Base delay between retries in seconds (default: 1.0)
- `rate_limit`: Maximum requests per minute (default: 100)

## Storage

The SDK includes an in-memory storage implementation, but you can create custom storage backends by implementing the `BaseStorage` interface:

```python
from typing import Any, Dict, Optional
from hunter_sdk.storage import BaseStorage

class CustomStorage(BaseStorage):
    def create(self, key: str, value: Dict[str, Any]) -> None:
        """Create a new record."""
        pass
    def read(self, key: str) -> Optional[Dict[str, Any]]:
        """Read a record."""
        pass
    def update(self, key: str, value: Dict[str, Any]) -> None:
        """Update an existing record."""
        pass
    def delete(self, key: str) -> None:
        """Delete a record."""
        pass
```

## Error Handling

The SDK defines several custom exceptions:

- `HunterSDKError`: Base exception for all SDK errors
- `ConfigurationError`: Raised when there's a configuration error
- `HunterAPIError`: Raised when the API returns an error response

Example error handling:

```python
from hunter_sdk.exceptions import HunterAPIError, ConfigurationError

try:
    result = client.verify_email('test@example.com')
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except HunterAPIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

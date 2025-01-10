"""Configuration module for Hunter SDK."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class HunterConfig:
    """Configuration class for Hunter API."""

    api_key: str
    base_url: str = 'https://api.hunter.io/v2'
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    rate_limit: Optional[int] = 100  # Requests per minute 
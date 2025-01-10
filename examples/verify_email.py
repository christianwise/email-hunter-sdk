"""Example usage of the Hunter SDK email verification service."""

from hunter_sdk import HunterClient, HunterConfig
from hunter_sdk.services import EmailVerificationService
from hunter_sdk.storage import MemoryStorage


def main() -> None:
    """Run email verification example."""
    # Initialize components
    config = HunterConfig(api_key='your-api-key-here')
    client = HunterClient(config)
    storage = MemoryStorage()
    service = EmailVerificationService(client, storage)

    # Example email to verify
    email = 'test@example.com'

    # First verification (will call API)
    print(f'Verifying {email}...')
    result = service.verify_email(email)
    print('Result:', result)

    # Second verification (will use cache)
    print(f'\nVerifying {email} again...')
    cached_result = service.verify_email(email)
    print('Cached result:', cached_result)

    # Force refresh (will call API again)
    print(f'\nForce refreshing verification for {email}...')
    fresh_result = service.verify_email(email, force_refresh=True)
    print('Fresh result:', fresh_result)


if __name__ == '__main__':
    main() 
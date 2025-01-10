"""Tests for storage implementations."""

import pytest

from hunter_sdk.storage import MemoryStorage


def test_memory_storage_create(memory_storage: MemoryStorage) -> None:
    """Test creating new records in memory storage."""
    test_data = {'key1': 'value1'}
    memory_storage.create('test', test_data)
    assert memory_storage.read('test') == test_data


def test_memory_storage_create_duplicate(memory_storage: MemoryStorage) -> None:
    """Test creating duplicate records raises KeyError."""
    memory_storage.create('test', {'data': 1})
    with pytest.raises(KeyError):
        memory_storage.create('test', {'data': 2})


def test_memory_storage_read_nonexistent(memory_storage: MemoryStorage) -> None:
    """Test reading nonexistent records returns None."""
    assert memory_storage.read('nonexistent') is None


def test_memory_storage_update(memory_storage: MemoryStorage) -> None:
    """Test updating existing records."""
    memory_storage.create('test', {'old': 'data'})
    memory_storage.update('test', {'new': 'data'})
    assert memory_storage.read('test') == {'new': 'data'}


def test_memory_storage_update_nonexistent(memory_storage: MemoryStorage) -> None:
    """Test updating nonexistent records raises KeyError."""
    with pytest.raises(KeyError):
        memory_storage.update('nonexistent', {'data': 1})


def test_memory_storage_delete(memory_storage: MemoryStorage) -> None:
    """Test deleting records."""
    memory_storage.create('test', {'data': 1})
    memory_storage.delete('test')
    assert memory_storage.read('test') is None


def test_memory_storage_delete_nonexistent(memory_storage: MemoryStorage) -> None:
    """Test deleting nonexistent records raises KeyError."""
    with pytest.raises(KeyError):
        memory_storage.delete('nonexistent') 
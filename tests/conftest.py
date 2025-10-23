from typing import Any, Dict, List

import pytest


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с примерами транзакций для тестирования функций обработки."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-12-25T15:30:45.123456", "amount": 100.0},
        {"id": 2, "state": "PENDING", "date": "2023-12-26T10:15:30.654321", "amount": 200.0},
        {"id": 3, "state": "EXECUTED", "date": "2023-12-24T18:45:12.987654", "amount": 150.0},
        {"id": 4, "state": "CANCELED", "date": "2023-12-27T09:20:05.555555", "amount": 300.0},
        {"id": 5, "state": "EXECUTED", "date": "2023-12-23T22:10:33.777777", "amount": 250.0},
    ]


@pytest.fixture
def sample_card_numbers() -> Dict[str, Any]:
    """Фикстура с примерами номеров карт для тестирования маскирования."""
    return {
        "valid_16": "1234567890123456",
        "valid_16_int": 1234567890123456,
        "valid_13": "1234567890123",
        "valid_19": "1234567890123456789",
        "valid_19_int": 1234567890123456789,
        "with_spaces": " 1234567890123456 ",
        "invalid_chars": "1234abcd5678efgh",
        "too_short": "123456789012",
        "too_long": "12345678901234567890",
    }


@pytest.fixture
def sample_account_numbers() -> Dict[str, Any]:
    """Фикстура с примерами номеров счетов для тестирования маскирования."""
    return {
        "valid": "12345678901234567890",
        "valid_int": 12345678901234567890,
        "short": "123",
        "with_spaces": " 12345678901234567890 ",
        "invalid_chars": "12345abcd67890",
    }


@pytest.fixture
def sample_card_strings() -> List[str]:
    """Фикстура с примерами строк для функции mask_account_card."""
    return [
        "Visa Platinum 7000792289606361",
        "Maestro 7000792289606361",
        "Mastercard 5555555555554444",
        "Счет 73654108430135874305",
        "Счет 1234 5678 9012 3456",
        "American Express 378282246310005",
        "InvalidString",
        "",
    ]


@pytest.fixture
def sample_dates() -> Dict[str, str]:
    """Фикстура с примерами дат для тестирования функции get_date."""
    return {
        "standard": "2024-03-11T02:26:18.671407",
        "different": "2023-12-25T15:30:45.123456",
        "without_microseconds": "2023-07-01T12:00:00",
        "invalid_format": "2023/12/25 15:30:45",
        "empty": "",
        "invalid_string": "not_a_date",
    }

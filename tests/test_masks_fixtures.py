from typing import Any, Dict

import pytest

from src.masks import format_in_blocks, get_mask_account, get_mask_card_number, only_digits


class TestOnlyDigitsFixtures:
    """Тесты для функции only_digits с использованием фикстур."""

    def test_only_digits_with_digits(self) -> None:
        """Проверка, что функция возвращает True для строки из цифр."""
        assert only_digits("123456") is True

    def test_only_digits_with_letters(self) -> None:
        """Проверка, что функция возвращает False для строки с буквами."""
        assert only_digits("abc123") is False

    def test_only_digits_with_special_chars(self) -> None:
        """Проверка, что функция возвращает False для строки со спецсимволами."""
        assert only_digits("123-456") is False

    def test_only_digits_empty_string(self) -> None:
        """Проверка, что функция возвращает False для пустой строки."""
        assert only_digits("") is False


class TestFormatInBlocksFixtures:
    """Тесты для функции format_in_blocks с использованием фикстур."""

    def test_format_in_blocks_default(self) -> None:
        """Проверка форматирования с размером блока по умолчанию."""
        assert format_in_blocks("1234567890123456") == "1234 5678 9012 3456"

    def test_format_in_blocks_custom_size(self) -> None:
        """Проверка форматирования с указанным размером блока."""
        assert format_in_blocks("1234567890123456", 6) == "123456 789012 3456"

    def test_format_in_blocks_empty_string(self) -> None:
        """Проверка форматирования пустой строки."""
        assert format_in_blocks("") == ""

    def test_format_in_blocks_short_string(self) -> None:
        """Проверка форматирования короткой строки."""
        assert format_in_blocks("123") == "123"


class TestGetMaskCardNumberFixtures:
    """Тесты для функции get_mask_card_number с использованием фикстур."""

    @pytest.mark.parametrize(
        "card_key, expected",
        [
            ("valid_16", "1234 56** **** 3456"),
            ("valid_13", "1234 56** *012 3"),
            ("valid_19", "1234 56** **** ***6 789"),
            ("valid_16_int", "1234 56** **** 3456"),
            ("with_spaces", "1234 56** **** 3456"),
        ],
    )
    def test_mask_card_number_valid_cases(
        self, sample_card_numbers: Dict[str, Any], card_key: str, expected: str
    ) -> None:
        """Проверка маскирования номеров карт в различных валидных случаях."""
        assert get_mask_card_number(sample_card_numbers[card_key]) == expected

    @pytest.mark.parametrize(
        "card_key, error_message",
        [
            ("invalid_chars", "Номер карты должен содержать только цифры"),
            ("too_short", "Длина номера карты должна быть от 13 до 19 цифр"),
            ("too_long", "Длина номера карты должна быть от 13 до 19 цифр"),
        ],
    )
    def test_mask_card_number_invalid_cases(
        self, sample_card_numbers: Dict[str, Any], card_key: str, error_message: str
    ) -> None:
        """Проверка вызова исключения при недопустимых номерах карт."""
        with pytest.raises(ValueError, match=error_message):
            get_mask_card_number(sample_card_numbers[card_key])


class TestGetMaskAccountFixtures:
    """Тесты для функции get_mask_account с использованием фикстур."""

    @pytest.mark.parametrize(
        "account_key, expected",
        [
            ("valid", "**7890"),
            ("short", "**123"),
            ("valid_int", "**7890"),
            ("with_spaces", "**7890"),
        ],
    )
    def test_mask_account_valid_cases(
        self, sample_account_numbers: Dict[str, Any], account_key: str, expected: str
    ) -> None:
        """Проверка маскирования номеров счетов в различных валидных случаях."""
        assert get_mask_account(sample_account_numbers[account_key]) == expected

    def test_mask_account_invalid_chars(self, sample_account_numbers: Dict[str, Any]) -> None:
        """Проверка вызова исключения при недопустимых символах."""
        with pytest.raises(ValueError, match="Номер счёта должен содержать только цифры"):
            get_mask_account(sample_account_numbers["invalid_chars"])

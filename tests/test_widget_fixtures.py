from typing import Dict, List

import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCardFixtures:
    """Тесты для функции mask_account_card с использованием фикстур."""

    @pytest.mark.parametrize(
        "string_index, expected",
        [
            (0, "Visa Platinum 7000 79** **** 6361"),
            (1, "Maestro 7000 79** **** 6361"),
            (2, "Mastercard 5555 55** **** 4444"),
            (3, "Счет **4305"),
            (4, "Счет **3456"),
            (5, "American Express 3782 82** ***0 005"),
        ],
    )
    def test_mask_account_card_valid_cases(
        self, sample_card_strings: List[str], string_index: int, expected: str
    ) -> None:
        """Проверка маскирования карт и счетов в различных валидных случаях."""
        assert mask_account_card(sample_card_strings[string_index]) == expected

    @pytest.mark.parametrize(
        "string_index",
        [
            6,  # InvalidString
            7,  # пустая строка
        ],
    )
    def test_mask_account_card_invalid_cases(self, sample_card_strings: List[str], string_index: int) -> None:
        """Проверка вызова исключения при неверном формате."""
        with pytest.raises(ValueError, match="Неверный формат входной строки"):
            mask_account_card(sample_card_strings[string_index])


class TestGetDateFixtures:
    """Тесты для функции get_date с использованием фикстур."""

    @pytest.mark.parametrize(
        "date_key, expected",
        [
            ("standard", "11.03.2024"),
            ("different", "25.12.2023"),
            ("without_microseconds", "01.07.2023"),
        ],
    )
    def test_get_date_valid_cases(self, sample_dates: Dict[str, str], date_key: str, expected: str) -> None:
        """Проверка преобразования дат в различных валидных форматах."""
        assert get_date(sample_dates[date_key]) == expected

    @pytest.mark.parametrize(
        "date_key",
        [
            "invalid_format",
            "empty",
            "invalid_string",
        ],
    )
    def test_get_date_invalid_cases(self, sample_dates: Dict[str, str], date_key: str) -> None:
        """Проверка вызова исключения при неверном формате даты."""
        with pytest.raises(ValueError, match="Неверный формат даты"):
            get_date(sample_dates[date_key])

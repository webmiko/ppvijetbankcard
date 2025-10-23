
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

    def test_mask_card_number_16_digits(self, sample_card_numbers) -> None:
        """Проверка маскирования 16-значного номера карты."""
        assert get_mask_card_number(sample_card_numbers["valid_16"]) == "1234 56** **** 3456"

    def test_mask_card_number_13_digits(self, sample_card_numbers) -> None:
        """Проверка маскирования 13-значного номера карты."""
        assert get_mask_card_number(sample_card_numbers["valid_13"]) == "1234 56** *012 3"

    def test_mask_card_number_19_digits(self, sample_card_numbers) -> None:
        """Проверка маскирования 19-значного номера карты."""
        assert get_mask_card_number(sample_card_numbers["valid_19"]) == "1234 56** **** ***6 789"

    def test_mask_card_number_int_input(self, sample_card_numbers) -> None:
        """Проверка работы с числовым вводом."""
        assert get_mask_card_number(sample_card_numbers["valid_16_int"]) == "1234 56** **** 3456"

    def test_mask_card_number_with_spaces(self, sample_card_numbers) -> None:
        """Проверка работы с номером карты, содержащим пробелы."""
        assert get_mask_card_number(sample_card_numbers["with_spaces"]) == "1234 56** **** 3456"

    def test_mask_card_number_invalid_chars(self, sample_card_numbers) -> None:
        """Проверка вызова исключения при недопустимых символах."""
        with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
            get_mask_card_number(sample_card_numbers["invalid_chars"])

    def test_mask_card_number_too_short(self, sample_card_numbers) -> None:
        """Проверка вызова исключения при слишком коротком номере."""
        with pytest.raises(ValueError, match="Длина номера карты должна быть от 13 до 19 цифр"):
            get_mask_card_number(sample_card_numbers["too_short"])

    def test_mask_card_number_too_long(self, sample_card_numbers) -> None:
        """Проверка вызова исключения при слишком длинном номере."""
        with pytest.raises(ValueError, match="Длина номера карты должна быть от 13 до 19 цифр"):
            get_mask_card_number(sample_card_numbers["too_long"])


class TestGetMaskAccountFixtures:
    """Тесты для функции get_mask_account с использованием фикстур."""

    def test_mask_account_normal(self, sample_account_numbers) -> None:
        """Проверка маскирования стандартного номера счета."""
        assert get_mask_account(sample_account_numbers["valid"]) == "**7890"

    def test_mask_account_short(self, sample_account_numbers) -> None:
        """Проверка маскирования короткого номера счета."""
        assert get_mask_account(sample_account_numbers["short"]) == "**123"

    def test_mask_account_int_input(self, sample_account_numbers) -> None:
        """Проверка работы с числовым вводом."""
        assert get_mask_account(sample_account_numbers["valid_int"]) == "**7890"

    def test_mask_account_with_spaces(self, sample_account_numbers) -> None:
        """Проверка работы с номером счета, содержащим пробелы."""
        assert get_mask_account(sample_account_numbers["with_spaces"]) == "**7890"

    def test_mask_account_invalid_chars(self, sample_account_numbers) -> None:
        """Проверка вызова исключения при недопустимых символах."""
        with pytest.raises(ValueError, match="Номер счёта должен содержать только цифры"):
            get_mask_account(sample_account_numbers["invalid_chars"])

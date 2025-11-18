import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты для функции mask_account_card."""

    def test_mask_account_card_card(self) -> None:
        """Проверка маскирования номера карты."""
        assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"

    def test_mask_account_card_account(self) -> None:
        """Проверка маскирования номера счета."""
        assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"

    def test_mask_account_card_card_single_word(self) -> None:
        """Проверка маскирования карты с одним словом в названии."""
        assert mask_account_card("Maestro 7000792289606361") == "Maestro 7000 79** **** 6361"

    def test_mask_account_card_card_multiple_words(self) -> None:
        """Проверка маскирования карты с несколькими словами в названии."""
        assert mask_account_card("American Express 7000792289606361") == "American Express 7000 79** **** 6361"

    def test_mask_account_card_account_with_spaces(self) -> None:
        """Проверка маскирования счета с пробелами."""
        assert mask_account_card("Счет  73654108430135874305") == "Счет **4305"

    def test_mask_account_card_invalid_format(self) -> None:
        """Проверка вызова исключения при неверном формате."""
        with pytest.raises(ValueError, match="Неверный формат входной строки"):
            mask_account_card("InvalidString")

    def test_mask_account_card_empty_string(self) -> None:
        """Проверка вызова исключения при пустой строке."""
        with pytest.raises(ValueError, match="Неверный формат входной строки"):
            mask_account_card("")


class TestGetDate:
    """Тесты для функции get_date."""

    def test_get_date_standard(self) -> None:
        """Проверка преобразования стандартной даты."""
        assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"

    def test_get_date_different_format(self) -> None:
        """Проверка преобразования даты в другом формате."""
        assert get_date("2023-12-25T15:30:45.123456") == "25.12.2023"

    def test_get_date_without_microseconds(self) -> None:
        """Проверка преобразования даты без микросекунд."""
        assert get_date("2023-07-01T12:00:00") == "01.07.2023"

    def test_get_date_invalid_format(self) -> None:
        """Проверка вызова исключения при неверном формате даты."""
        with pytest.raises(ValueError, match="Неверный формат даты"):
            get_date("2023/12/25 15:30:45")

    def test_get_date_empty_string(self) -> None:
        """Проверка вызова исключения при пустой строке."""
        with pytest.raises(ValueError, match="Неверный формат даты"):
            get_date("")

    def test_get_date_invalid_string(self) -> None:
        """Проверка вызова исключения при недопустимой строке."""
        with pytest.raises(ValueError, match="Неверный формат даты"):
            get_date("not_a_date")

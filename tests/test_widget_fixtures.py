
import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCardFixtures:
    """Тесты для функции mask_account_card с использованием фикстур."""

    def test_mask_account_card_card(self, sample_card_strings) -> None:
        """Проверка маскирования номера карты."""
        assert mask_account_card(sample_card_strings[0]) == "Visa Platinum 7000 79** **** 6361"

    def test_mask_account_card_account(self, sample_card_strings) -> None:
        """Проверка маскирования номера счета."""
        assert mask_account_card(sample_card_strings[3]) == "Счет **4305"

    def test_mask_account_card_card_single_word(self, sample_card_strings) -> None:
        """Проверка маскирования карты с одним словом в названии."""
        assert mask_account_card(sample_card_strings[1]) == "Maestro 7000 79** **** 6361"

    def test_mask_account_card_card_multiple_words(self, sample_card_strings) -> None:
        """Проверка маскирования карты с несколькими словами в названии."""
        assert mask_account_card(sample_card_strings[4]) == "Счет **3456"

    def test_mask_account_card_account_with_spaces(self, sample_card_strings) -> None:
        """Проверка маскирования счета с пробелами."""
        assert mask_account_card(sample_card_strings[4]) == "Счет **3456"

    def test_mask_account_card_invalid_format(self, sample_card_strings) -> None:
        """Проверка вызова исключения при неверном формате."""
        with pytest.raises(ValueError, match="Неверный формат входной строки"):
            mask_account_card(sample_card_strings[6])

    def test_mask_account_card_empty_string(self, sample_card_strings) -> None:
        """Проверка вызова исключения при пустой строке."""
        with pytest.raises(ValueError, match="Неверный формат входной строки"):
            mask_account_card(sample_card_strings[7])


class TestGetDateFixtures:
    """Тесты для функции get_date с использованием фикстур."""

    def test_get_date_standard(self, sample_dates) -> None:
        """Проверка преобразования стандартной даты."""
        assert get_date(sample_dates["standard"]) == "11.03.2024"

    def test_get_date_different_format(self, sample_dates) -> None:
        """Проверка преобразования даты в другом формате."""
        assert get_date(sample_dates["different"]) == "25.12.2023"

    def test_get_date_without_microseconds(self, sample_dates) -> None:
        """Проверка преобразования даты без микросекунд."""
        assert get_date(sample_dates["without_microseconds"]) == "01.07.2023"

    def test_get_date_invalid_format(self, sample_dates) -> None:
        """Проверка вызова исключения при неверном формате даты."""
        with pytest.raises(ValueError, match="Неверный формат даты"):
            get_date(sample_dates["invalid_format"])

    def test_get_date_empty_string(self, sample_dates) -> None:
        """Проверка вызова исключения при пустой строке."""
        with pytest.raises(ValueError, match="Неверный формат даты"):
            get_date(sample_dates["empty"])

    def test_get_date_invalid_string(self, sample_dates) -> None:
        """Проверка вызова исключения при недопустимой строке."""
        with pytest.raises(ValueError, match="Неверный формат даты"):
            get_date(sample_dates["invalid_string"])

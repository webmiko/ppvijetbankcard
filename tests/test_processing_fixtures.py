
from typing import Any

from src.processing import filter_by_state, sort_by_date


class TestFilterByStateFixtures:
    """Тесты для функции filter_by_state с использованием фикстур."""

    def test_filter_by_state_default(self, sample_transactions) -> None:
        """Проверка фильтрации по состоянию EXECUTED (по умолчанию)."""
        result = filter_by_state(sample_transactions)
        assert len(result) == 3
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3
        assert result[2]["id"] == 5

    def test_filter_by_state_custom(self, sample_transactions) -> None:
        """Проверка фильтрации по пользовательскому состоянию."""
        result = filter_by_state(sample_transactions, "PENDING")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_by_state_empty(self) -> None:
        """Проверка фильтрации пустого списка."""
        assert filter_by_state([]) == []

    def test_filter_by_state_no_match(self, sample_transactions) -> None:
        """Проверка фильтрации без совпадений."""
        result = filter_by_state(sample_transactions, "NONEXISTENT")
        assert result == []

    def test_filter_by_state_missing_state_key(self) -> None:
        """Проверка обработки транзакций без ключа state."""
        transactions: list[dict[str, Any]] = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2},  # Без ключа state
            {"id": 3, "state": "EXECUTED"},
        ]
        result = filter_by_state(transactions)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3


class TestSortByDateFixtures:
    """Тесты для функции sort_by_date с использованием фикстур."""

    def test_sort_by_date_descending(self, sample_transactions) -> None:
        """Проверка сортировки по убыванию (по умолчанию)."""
        result = sort_by_date(sample_transactions)
        assert result[0]["id"] == 4  # 27 декабря
        assert result[1]["id"] == 2  # 26 декабря
        assert result[2]["id"] == 1  # 25 декабря
        assert result[3]["id"] == 3  # 24 декабря
        assert result[4]["id"] == 5  # 23 декабря

    def test_sort_by_date_ascending(self, sample_transactions) -> None:
        """Проверка сортировки по возрастанию."""
        result = sort_by_date(sample_transactions, is_reverse_order=False)
        assert result[0]["id"] == 5  # 23 декабря
        assert result[1]["id"] == 3  # 24 декабря
        assert result[2]["id"] == 1  # 25 декабря
        assert result[3]["id"] == 2  # 26 декабря
        assert result[4]["id"] == 4  # 27 декабря

    def test_sort_by_date_empty(self) -> None:
        """Проверка сортировки пустого списка."""
        assert sort_by_date([]) == []

    def test_sort_by_date_same_dates(self) -> None:
        """Проверка сортировки с одинаковыми датами."""
        base_date = "2023-03-11T02:26:18.671407"
        transactions = [{"id": 1, "date": base_date}, {"id": 2, "date": base_date}, {"id": 3, "date": base_date}]
        result = sort_by_date(transactions)
        assert len(result) == 3
        # Порядок должен сохраниться при одинаковых датах
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2
        assert result[2]["id"] == 3

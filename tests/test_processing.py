from typing import Any

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    def test_filter_by_state_default(self) -> None:
        """Проверка фильтрации по состоянию EXECUTED (по умолчанию)."""
        transactions = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "PENDING"},
            {"id": 3, "state": "EXECUTED"},
            {"id": 4, "state": "CANCELED"},
        ]
        result = filter_by_state(transactions)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3

    def test_filter_by_state_custom(self) -> None:
        """Проверка фильтрации по пользовательскому состоянию."""
        transactions = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "PENDING"},
            {"id": 3, "state": "PENDING"},
            {"id": 4, "state": "CANCELED"},
        ]
        result = filter_by_state(transactions, "PENDING")
        assert len(result) == 2
        assert result[0]["id"] == 2
        assert result[1]["id"] == 3

    def test_filter_by_state_empty(self) -> None:
        """Проверка фильтрации пустого списка."""
        assert filter_by_state([]) == []

    def test_filter_by_state_no_match(self) -> None:
        """Проверка фильтрации без совпадений."""
        transactions = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "EXECUTED"}]
        result = filter_by_state(transactions, "PENDING")
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


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_sort_by_date_descending(self) -> None:
        """Проверка сортировки по убыванию (по умолчанию)."""
        transactions = [
            {"id": 1, "date": "2023-03-11T02:26:18.671407"},
            {"id": 2, "date": "2023-04-15T10:30:00.123456"},
            {"id": 3, "date": "2023-02-05T18:45:30.987654"},
        ]
        result = sort_by_date(transactions)
        assert result[0]["id"] == 2  # Апрель
        assert result[1]["id"] == 1  # Март
        assert result[2]["id"] == 3  # Февраль

    def test_sort_by_date_ascending(self) -> None:
        """Проверка сортировки по возрастанию."""
        transactions = [
            {"id": 1, "date": "2023-03-11T02:26:18.671407"},
            {"id": 2, "date": "2023-04-15T10:30:00.123456"},
            {"id": 3, "date": "2023-02-05T18:45:30.987654"},
        ]
        result = sort_by_date(transactions, is_reverse_order=False)
        assert result[0]["id"] == 3  # Февраль
        assert result[1]["id"] == 1  # Март
        assert result[2]["id"] == 2  # Апрель

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

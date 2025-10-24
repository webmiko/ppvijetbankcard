from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByStateFixtures:
    """Тесты для функции filter_by_state с использованием фикстур."""

    @pytest.mark.parametrize(
        "state, expected_ids",
        [
            ("EXECUTED", [1, 3, 5]),
            ("PENDING", [2]),
            ("CANCELED", [4]),
            ("NONEXISTENT", []),
        ],
    )
    def test_filter_by_state(
        self, sample_transactions: List[Dict[str, Any]], state: str, expected_ids: List[int]
    ) -> None:
        """Проверка фильтрации по различным состояниям."""
        result = filter_by_state(sample_transactions, state)
        assert [t["id"] for t in result] == expected_ids

    def test_filter_by_state_empty(self) -> None:
        """Проверка фильтрации пустого списка."""
        assert filter_by_state([]) == []

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

    @pytest.mark.parametrize(
        "is_reverse_order, expected_ids",
        [
            (True, [4, 2, 1, 3, 5]),  # по убыванию (по умолчанию)
            (False, [5, 3, 1, 2, 4]),  # по возрастанию
        ],
    )
    def test_sort_by_date(
        self, sample_transactions: List[Dict[str, Any]], is_reverse_order: bool, expected_ids: List[int]
    ) -> None:
        """Проверка сортировки по дате в различных направлениях."""
        result = sort_by_date(sample_transactions, is_reverse_order=is_reverse_order)
        assert [t["id"] for t in result] == expected_ids

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

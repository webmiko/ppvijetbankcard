from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        transactions: Список словарей для фильтрации
        state: Значение состояния для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Новый список, содержащий только словари с указанным значением состояния
    """
    # Используем .get() для безопасного доступа к ключу, чтобы избежать KeyError
    return [tx for tx in transactions if tx.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], is_reverse_order: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по ключу 'date' в формате ISO.

    Args:
        transactions: Список словарей, содержащих ключи 'date'
        is_reverse_order: Порядок сортировки (по умолчанию True - по убыванию)

    Returns:
        Новый список, отсортированный по дате
    """
    # Сортировка с использованием преобразования строки даты в объект datetime
    # Явно указываем тип данных для ключа сортировки, чтобы улучшить читаемость
    return sorted(
        transactions,
        key=lambda tx: datetime.fromisoformat(tx["date"]),
        reverse=is_reverse_order
    )

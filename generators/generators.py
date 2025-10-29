from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency_code: Код валюты для фильтрации (например, "USD")

    Yields:
        Словари транзакций, у которых валюта соответствует заданной
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Возвращает описание каждой операции по очереди.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описание операции из каждой транзакции
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.
    Генерирует номера от 0000 0000 0000 0001 до 9999 9999 9999 9999.

    Args:
        start: Начальное значение для генерации
        end: Конечное значение для генерации

    Yields:
        Отформатированные номера карт
    """
    for number in range(start, end + 1):
        # Форматируем число в 16-значную строку с ведущими нулями
        card_number = f"{number:016d}"
        # Разделяем на группы по 4 цифры и добавляем пробелы
        formatted = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted

from .widget import get_date, mask_account_card


def filter_by_state(list_of_dicts: list, state: str = "EXECUTED") -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        list_of_dicts: Список словарей для фильтрации
        state: Значение состояния для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Новый список, содержащий только словари с указанным значением состояния
    """
    return [item for item in list_of_dicts if item.get("state") == state]


def sort_by_date(list_of_dicts: list, reverse_order: bool = True) -> list:
    """
    Сортирует список словарей по ключу 'date' в формате ISO.

    Args:
        list_of_dicts: Список словарей, содержащих ключи 'date'
        reverse_order: Порядок сортировки (по умолчанию True - по убыванию)

    Returns:
        Новый список, отсортированный по дате
    """
    return sorted(list_of_dicts, key=lambda x: x["date"], reverse=reverse_order)


######################################
# Функции для демонстрации работы масок
def format_transactions(transactions: list, state: str = "EXECUTED", reverse_order: bool = True) -> list:
    """
    Обрабатывает и форматирует список транзакций для отображения.

    Args:
        transactions: Список словарей с транзакциями
        state: Значение состояния для фильтрации (по умолчанию 'EXECUTED')
        reverse_order: Порядок сортировки по дате (по умолчанию True - по убыванию)

    Returns:
        Новый список с отформатированными транзакциями
    """
    # Фильтруем транзакции по состоянию
    filtered = filter_by_state(transactions, state)

    # Сортируем по дате
    sorted_transactions = sort_by_date(filtered, reverse_order)

    # Форматируем каждую транзакцию для отображения
    formatted_transactions = []
    for transaction in sorted_transactions:
        # Создаем копию, чтобы не изменять оригинальный словарь
        formatted = transaction.copy()

        # Форматируем дату
        if "date" in formatted:
            formatted["date"] = get_date(formatted["date"])

        # Маскируем номер карты или счета, если они есть
        if "from" in formatted:
            formatted["from"] = mask_account_card(formatted["from"])
        if "to" in formatted:
            formatted["to"] = mask_account_card(formatted["to"])

        formatted_transactions.append(formatted)

    return formatted_transactions


def mask_transaction_details(transaction: dict) -> dict:
    """
    Маскирует чувствительные данные в одной транзакции.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Новый словарь с замаскированными данными
    """
    # Создаем копию, чтобы не изменять оригинальный словарь
    masked = transaction.copy()

    # Маскируем номер карты или счета, если они есть
    if "from" in masked:
        masked["from"] = mask_account_card(masked["from"])
    if "to" in masked:
        masked["to"] = mask_account_card(masked["to"])

    return masked


def get_formatted_date(transaction: dict) -> dict:
    """
    Форматирует дату в одной транзакции.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Новый словарь с отформатированной датой
    """
    # Создаем копию, чтобы не изменять оригинальный словарь
    formatted = transaction.copy()

    # Форматируем дату, если она есть
    if "date" in formatted:
        formatted["date"] = get_date(formatted["date"])

    return formatted

def filter_by_state(list_of_dicts: list, state: str = 'EXECUTED') -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        list_of_dicts: Список словарей для фильтрации
        state: Значение состояния для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Новый список, содержащий только словари с указанным значением состояния
    """
    return [item for item in list_of_dicts if item.get('state') == state]


def sort_by_date(list_of_dicts: list, reverse_order: bool = True) -> list:
    """
    Сортирует список словарей по ключу 'date' в формате ISO.

    Args:
        list_of_dicts: Список словарей, содержащих ключи 'date'
        reverse_order: Порядок сортировки (по умолчанию True - по убыванию)

    Returns:
        Новый список, отсортированный по дате
    """
    return sorted(list_of_dicts, key=lambda x: x['date'], reverse=reverse_order)

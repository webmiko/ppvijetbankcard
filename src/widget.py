from .masks import get_mask_card_number, get_mask_account
from datetime import datetime


def mask_account_card(input_string: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.

    Args:
        input_string: Строка вида "Visa Platinum 7000792289606361" или "Счет 73654108430135874305"

    Returns:
        Строка с замаскированным номером карты или счета

    Examples:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        "Visa Platinum 7000 79** **** 6361"
        >>> mask_account_card("Счет 73654108430135874305")
        "Счет **4305"
    """
    # Разделяем строку на части
    card_parts = input_string.split()

    if len(card_parts) < 2:
        raise ValueError("Неверный формат входной строки")

    # Определяем тип (карта или счет)
    if card_parts[0] == "Счет":
        # Для счета берем все части кроме первой как номер
        account_number = "".join(card_parts[1:])
        masked_number = get_mask_account(account_number)
        return f"Счет {masked_number}"
    else:
        # Для карты берем последнюю часть как номер карты
        card_number = card_parts[-1]
        card_type = " ".join(card_parts[:-1])
        masked_number = get_mask_card_number(card_number)
        return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из ISO формата в формат ДД.ММ.ГГГГ.

    Args:
        date_string: Строка с датой в формате "2024-03-11T02:26:18.671407"

    Returns:
        Строка с датой в формате "11.03.2024"

    Examples:
        >>> get_date("2024-03-11T02:26:18.671407")
        "11.03.2024"
        >>> get_date("2023-12-25T15:30:45.123456")
        "25.12.2023"
    """
    try:
        # Преобразуем дату из ISO формата
        date_time = datetime.fromisoformat(date_string)
        # Форматируем в нужный формат ДД.ММ.ГГГГ
        return date_time.strftime("%d.%m.%Y")
    except ValueError as e:
        raise ValueError(f"Неверный формат даты: {e}")

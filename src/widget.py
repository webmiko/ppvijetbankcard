from .masks import get_mask_card_number, get_mask_account


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

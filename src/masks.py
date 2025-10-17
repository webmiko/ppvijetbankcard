def only_digits(value: str) -> bool:
    """Возвращает True, если строка состоит только из цифр."""
    return value.isdigit()


def format_in_blocks(text: str, block_size: int = 4) -> str:
    """Возвращает строку, разбитую пробелами на блоки по block_size символов."""
    if not text:
        return text
    return " ".join(text[i : i + block_size] for i in range(0, len(text), block_size))


def get_mask_card_number(card_number: int | str) -> str:
    """
    Маскирует номер карты.

    По умолчанию показываются первые 6 и последние 4 цифры, остальное скрывается звёздочками.
    Для классического 16-значного PAN формируется вид: "XXXX XX** **** XXXX".

    Args:
        card_number: Номер карты (целое число или строка из цифр)

    Returns:
        Замаскированный номер карты в виде строки

    Raises:
        ValueError: если встречаются нецифровые символы или длина вне [13, 19]
    """
    card_str = str(card_number).strip()

    if not only_digits(card_str):
        raise ValueError("Номер карты должен содержать только цифры")

    length = len(card_str)
    if length < 13 or length > 19:
        raise ValueError("Длина номера карты должна быть от 13 до 19 цифр")

    # Для 16-значного номера фиксированная расстановка пробелов: XXXX XX** **** XXXX
    if length == 16:
        return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    else:
        # Для прочих длин: первые 6, звёздочки, последние 4
        first6 = card_str[:6]
        last4 = card_str[-4:]
        middle_len = max(0, length - 10)
        masked_middle = "*" * middle_len
        masked_raw = f"{first6}{masked_middle}{last4}"

    # Возвращаем строку, разбитую пробелами каждые 4 символа
    return format_in_blocks(masked_raw)


def get_mask_account(account_number: int | str) -> str:
    """
    Маскирует номер счёта: показывает только последние 4 цифры, добавляя префикс "**".

    Args:
        account_number: Номер счёта (целое число или строка из цифр)

    Returns:
        Замаскированный номер счёта в виде строки

    Raises:
        ValueError: если встречаются нецифровые символы
    """
    acc_str = str(account_number).strip()

    if not only_digits(acc_str):
        raise ValueError("Номер счёта должен содержать только цифры")

    tail = acc_str[-4:] if len(acc_str) >= 4 else acc_str
    masked_raw = f"**{tail}"
    # Для маски счёта пробелы не требуются
    return masked_raw

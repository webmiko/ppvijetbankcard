from src.logger_config import setup_logger

logger = setup_logger("masks")


def only_digits(value: str) -> bool:
    """Возвращает True, если строка состоит только из цифр."""
    logger.debug(f"Проверка строки на наличие только цифр: {value}")
    result = value.isdigit()
    logger.info(f"Результат проверки: {result}")
    return result


def format_in_blocks(text: str, block_size: int = 4) -> str:
    """Возвращает строку, разбитую пробелами на блоки по block_size символов."""
    logger.debug(f"Форматирование строки в блоки: text={text}, block_size={block_size}")
    if not text:
        logger.debug("Пустая строка, возврат без изменений")
        return text
    result = " ".join(text[i : i + block_size] for i in range(0, len(text), block_size))
    logger.info(f"Результат форматирования: {result}")
    return result


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
    logger.info(f"Начало маскировки номера карты: {card_number}")
    card_str = str(card_number).strip()

    if not only_digits(card_str):
        error_msg = "Номер карты должен содержать только цифры"
        logger.error(f"Ошибка при маскировке номера карты {card_number}: {error_msg}")
        raise ValueError(error_msg)

    length = len(card_str)
    if length < 13 or length > 19:
        error_msg = "Длина номера карты должна быть от 13 до 19 цифр"
        logger.error(f"Ошибка при маскировке номера карты {card_number}: {error_msg}")
        raise ValueError(error_msg)

    # Для 16-значного номера фиксированная расстановка пробелов: XXXX XX** **** XXXX
    if length == 16:
        masked_number = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    else:
        # Для прочих длин: первые 6, звёздочки, последние 4
        first6 = card_str[:6]
        last4 = card_str[-4:]
        middle_len = max(0, length - 10)
        masked_middle = "*" * middle_len
        masked_raw = f"{first6}{masked_middle}{last4}"
        # Возвращаем строку, разбитую пробелами каждые 4 символа
        masked_number = format_in_blocks(masked_raw)

    logger.info(f"Номер карты успешно замаскирован: {masked_number}")
    return masked_number


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
    logger.info(f"Начало маскировки номера счета: {account_number}")
    acc_str = str(account_number).strip()

    if not only_digits(acc_str):
        error_msg = "Номер счёта должен содержать только цифры"
        logger.error(f"Ошибка при маскировке номера счета {account_number}: {error_msg}")
        raise ValueError(error_msg)

    tail = acc_str[-4:] if len(acc_str) >= 4 else acc_str
    masked_account = f"**{tail}"
    logger.info(f"Номер счета успешно замаскирован: {masked_account}")
    # Для маски счёта пробелы не требуются
    return masked_account

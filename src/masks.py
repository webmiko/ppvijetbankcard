from src.logger_config import setup_logger

logger = setup_logger("masks")

# Константы для маскировки карт и счетов
DEFAULT_BLOCK_SIZE = 4
MIN_CARD_LENGTH = 13
MAX_CARD_LENGTH = 19
STANDARD_CARD_LENGTH = 16
VISIBLE_CARD_PREFIX_LENGTH = 6  # Первые 6 цифр для нестандартных карт
VISIBLE_CARD_SUFFIX_LENGTH = 4  # Последние 4 цифры
STANDARD_CARD_FIRST_PART_LENGTH = 4  # Первые 4 цифры для стандартной карты
STANDARD_CARD_SECOND_PART_LENGTH = 2  # Следующие 2 цифры для стандартной карты
STANDARD_CARD_MASKED_PART_LENGTH = 4  # Количество звездочек в середине стандартной карты
VISIBLE_ACCOUNT_SUFFIX_LENGTH = 4
CARD_MASK_SYMBOL = "*"
ACCOUNT_MASK_PREFIX = "**"
# Расчет: MIN_CARD_LENGTH - VISIBLE_CARD_PREFIX_LENGTH - VISIBLE_CARD_SUFFIX_LENGTH
CARD_MIDDLE_PART_CALCULATION = MIN_CARD_LENGTH - VISIBLE_CARD_PREFIX_LENGTH - VISIBLE_CARD_SUFFIX_LENGTH


def only_digits(value: str) -> bool:
    """Возвращает True, если строка состоит только из цифр."""
    logger.debug(f"Проверка строки на наличие только цифр: {value}")
    result = value.isdigit()
    logger.info(f"Результат проверки: {result}")
    return result


def format_in_blocks(text: str, block_size: int = DEFAULT_BLOCK_SIZE) -> str:
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
    if length < MIN_CARD_LENGTH or length > MAX_CARD_LENGTH:
        error_msg = f"Длина номера карты должна быть от {MIN_CARD_LENGTH} до {MAX_CARD_LENGTH} цифр"
        logger.error(f"Ошибка при маскировке номера карты {card_number}: {error_msg}")
        raise ValueError(error_msg)

    # Для стандартной длины карты фиксированная расстановка пробелов: XXXX XX** **** XXXX
    if length == STANDARD_CARD_LENGTH:
        # Первые 4 цифры, затем 2 цифры, затем 4 звездочки, затем последние 4 цифры
        first_part = card_str[:STANDARD_CARD_FIRST_PART_LENGTH]
        second_part_start = STANDARD_CARD_FIRST_PART_LENGTH
        second_part_end = STANDARD_CARD_FIRST_PART_LENGTH + STANDARD_CARD_SECOND_PART_LENGTH
        second_part = card_str[second_part_start:second_part_end]
        masked_part = CARD_MASK_SYMBOL * STANDARD_CARD_MASKED_PART_LENGTH
        last_part = card_str[-VISIBLE_CARD_SUFFIX_LENGTH:]
        masked_number = f"{first_part} {second_part}{CARD_MASK_SYMBOL}{CARD_MASK_SYMBOL} {masked_part} {last_part}"
    else:
        # Для прочих длин: первые 6, звёздочки, последние 4
        first6 = card_str[:VISIBLE_CARD_PREFIX_LENGTH]
        last4 = card_str[-VISIBLE_CARD_SUFFIX_LENGTH:]
        middle_len = max(0, length - CARD_MIDDLE_PART_CALCULATION)
        masked_middle = CARD_MASK_SYMBOL * middle_len
        masked_raw = f"{first6}{masked_middle}{last4}"
        # Возвращаем строку, разбитую пробелами каждые DEFAULT_BLOCK_SIZE символа
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

    if len(acc_str) >= VISIBLE_ACCOUNT_SUFFIX_LENGTH:
        tail = acc_str[-VISIBLE_ACCOUNT_SUFFIX_LENGTH:]
    else:
        tail = acc_str
    masked_account = f"{ACCOUNT_MASK_PREFIX}{tail}"
    logger.info(f"Номер счета успешно замаскирован: {masked_account}")
    # Для маски счёта пробелы не требуются
    return masked_account

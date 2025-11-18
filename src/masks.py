import logging
from pathlib import Path


def _setup_logger() -> logging.Logger:
    """
    Настраивает и возвращает логгер для модуля masks.

    Returns:
        Настроенный логгер для модуля masks
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Предотвращаем дублирование логов (если логгер уже настроен)
    if logger.handlers:
        return logger

    # Создаем директорию logs, если её нет
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Создаем обработчик для записи в файл
    log_file = logs_dir / "masks.log"
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Создаем форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger


# Создаем логгер для модуля
logger = _setup_logger()


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
    logger.debug(f"Начало маскирования номера карты: {type(card_number)}")

    card_str = str(card_number).strip()

    if not only_digits(card_str):
        logger.error(f"Номер карты содержит нецифровые символы: {card_str}")
        raise ValueError("Номер карты должен содержать только цифры")

    length = len(card_str)
    if length < 13 or length > 19:
        logger.error(f"Некорректная длина номера карты: {length}")
        raise ValueError("Длина номера карты должна быть от 13 до 19 цифр")

    logger.debug(f"Длина номера карты: {length}")

    # Для 16-значного номера фиксированная расстановка пробелов: XXXX XX** **** XXXX
    if length == 16:
        result = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    else:
        # Для прочих длин: первые 6, звёздочки, последние 4
        first6 = card_str[:6]
        last4 = card_str[-4:]
        middle_len = max(0, length - 10)
        masked_middle = "*" * middle_len
        masked_raw = f"{first6}{masked_middle}{last4}"

        # Возвращаем строку, разбитую пробелами каждые 4 символа
        result = format_in_blocks(masked_raw)

    logger.info(f"Номер карты успешно замаскирован, длина: {length}")
    return result


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
    logger.debug(f"Начало маскирования номера счёта: {type(account_number)}")

    acc_str = str(account_number).strip()

    if not only_digits(acc_str):
        logger.error(f"Номер счёта содержит нецифровые символы: {acc_str}")
        raise ValueError("Номер счёта должен содержать только цифры")

    tail = acc_str[-4:] if len(acc_str) >= 4 else acc_str
    masked_raw = f"**{tail}"
    # Для маски счёта пробелы не требуются

    logger.info(f"Номер счёта успешно замаскирован, длина: {len(acc_str)}")
    return masked_raw

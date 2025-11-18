"""Модуль для настройки логирования в проекте."""

import logging
from pathlib import Path

# Константы для настройки логирования
LOGS_DIR_NAME = "logs"
LOG_FILE_MODE = "w"  # Режим перезаписи при каждом запуске
ENCODING = "utf-8"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_LEVEL = logging.INFO


def setup_logger(module_name: str) -> logging.Logger:
    """
    Создает и настраивает логер для указанного модуля.

    Логер записывает логи в файл с перезаписью при каждом запуске приложения.
    Формат записи: метка времени, название модуля, уровень серьезности, сообщение.

    Args:
        module_name: Имя модуля для которого создается логер (например, "masks" или "utils")

    Returns:
        Настроенный объект логера для указанного модуля
    """
    # Определяем корень проекта (родительский каталог папки src)
    project_root = Path(__file__).parent.parent
    logs_dir = project_root / LOGS_DIR_NAME

    # Создаем папку logs/ если её нет
    logs_dir.mkdir(exist_ok=True)

    # Путь к файлу лога
    log_file = logs_dir / f"{module_name}.log"

    # Создаем логер с именем модуля
    logger = logging.getLogger(module_name)

    # Устанавливаем уровень логирования
    logger.setLevel(DEFAULT_LOG_LEVEL)

    # Очищаем существующие обработчики (чтобы избежать дублирования)
    logger.handlers.clear()

    # Создаем FileHandler с режимом перезаписи при каждом запуске
    handler = logging.FileHandler(log_file, mode=LOG_FILE_MODE, encoding=ENCODING)

    # Создаем форматтер с нужным форматом
    # Формат: метка времени - название модуля - уровень серьезности - сообщение
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Устанавливаем форматтер для обработчика
    handler.setFormatter(formatter)

    # Добавляем обработчик к логеру
    logger.addHandler(handler)

    return logger

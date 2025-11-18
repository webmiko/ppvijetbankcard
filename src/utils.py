import json
import os
from typing import Any, Dict, List

from src.logger_config import setup_logger

logger = setup_logger("utils")


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Args:
        file_path: Путь до JSON-файла с транзакциями

    Returns:
        Список словарей с данными о финансовых транзакциях.
        Возвращает пустой список, если:
        - файл не найден
        - файл пустой
        - файл содержит не список (например, словарь)
        - произошла ошибка при парсинге JSON
    """
    logger.info(f"Начало загрузки транзакций из файла: {file_path}")

    # Проверяем существование файла
    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден: {file_path}")
        return []

    logger.debug(f"Файл найден: {file_path}")

    try:
        # Открываем файл в режиме чтения
        logger.debug(f"Чтение содержимого файла: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            # Читаем содержимое файла
            content = file.read().strip()

            # Если файл пустой, возвращаем пустой список
            if not content:
                logger.warning(f"Файл пустой: {file_path}")
                return []

            # Парсим JSON
            logger.debug(f"Парсинг JSON из файла: {file_path}")
            data = json.loads(content)

            # Проверяем, что результат является списком
            if not isinstance(data, list):
                logger.warning(f"Данные в файле не являются списком: {file_path}")
                return []

            # Возвращаем список транзакций
            logger.info(f"Успешно загружено {len(data)} транзакций из файла: {file_path}")
            return data

    except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
        # Обрабатываем возможные ошибки:
        # - FileNotFoundError: файл не найден (хотя мы уже проверили через os.path.exists)
        # - json.JSONDecodeError: невалидный JSON
        # - OSError: ошибки при чтении файла
        error_msg = str(e)
        logger.error(f"Ошибка при загрузке транзакций из файла {file_path}: {error_msg}", exc_info=True)
        return []

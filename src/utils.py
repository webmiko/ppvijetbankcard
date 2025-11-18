import json
import os
from typing import Any, Dict, List


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
    # Проверяем существование файла
    if not os.path.exists(file_path):
        return []

    try:
        # Открываем файл в режиме чтения
        with open(file_path, "r", encoding="utf-8") as file:
            # Читаем содержимое файла
            content = file.read().strip()

            # Если файл пустой, возвращаем пустой список
            if not content:
                return []

            # Парсим JSON
            data = json.loads(content)

            # Проверяем, что результат является списком
            if not isinstance(data, list):
                return []

            # Возвращаем список транзакций
            return data

    except (FileNotFoundError, json.JSONDecodeError, OSError):
        # Обрабатываем возможные ошибки:
        # - FileNotFoundError: файл не найден (хотя мы уже проверили через os.path.exists)
        # - json.JSONDecodeError: невалидный JSON
        # - OSError: ошибки при чтении файла
        return []

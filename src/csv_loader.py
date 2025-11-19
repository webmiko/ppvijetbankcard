import logging
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd  # type: ignore[import-untyped]
from pandas import isna  # type: ignore[import-untyped]


def _setup_logger() -> logging.Logger:
    """
    Настраивает и возвращает логгер для модуля csv_loader.

    Returns:
        Настроенный логгер для модуля csv_loader
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "csv_loader.log"
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


# Создаем логгер для модуля
logger = _setup_logger()

# 4. Константы модуля
ENCODING = "utf-8"
DEFAULT_RETURN_VALUE: List[Dict[str, Any]] = []
CSV_SEPARATOR = ";"  # Разделитель для CSV файлов

# 5. Функции модуля


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из CSV-файла.

    Args:
        file_path: Путь до CSV-файла с транзакциями

    Returns:
        Список словарей с данными о финансовых транзакциях.
        Возвращает пустой список, если:
        - файл не найден
        - произошла ошибка при чтении CSV
    """
    logger.debug(f"Начало загрузки транзакций из CSV файла: {file_path}")

    # Проверяем существование файла
    if not Path(file_path).exists():
        logger.warning(f"Файл не найден: {file_path}")
        return DEFAULT_RETURN_VALUE

    try:
        # Чтение CSV через pandas
        df = pd.read_csv(file_path, sep=CSV_SEPARATOR, encoding=ENCODING)

        # Преобразование DataFrame в список словарей
        transactions_raw = df.to_dict("records")

        # Преобразование типов для соответствия формату JSON (числа могут быть float)
        transactions: List[Dict[str, Any]] = []
        for transaction_raw in transactions_raw:
            transaction: Dict[str, Any] = {}
            for key, value in transaction_raw.items():
                # Пропускаем NaN значения
                if isna(value):
                    continue
                # Преобразуем float в int для id, если возможно
                if key == "id" and isinstance(value, float):
                    transaction[key] = int(value)
                # Преобразуем float в str для amount, если нужно
                elif key == "amount" and isinstance(value, float):
                    transaction[key] = str(value)
                else:
                    transaction[key] = value
            transactions.append(transaction)

        logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV файла: {file_path}")
        return transactions

    except pd.errors.EmptyDataError:
        logger.warning(f"CSV файл пустой: {file_path}")
        return DEFAULT_RETURN_VALUE
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV файла {file_path}: {type(e).__name__} - {e}")
        return DEFAULT_RETURN_VALUE


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из Excel-файла (XLSX).

    Args:
        file_path: Путь до Excel-файла с транзакциями

    Returns:
        Список словарей с данными о финансовых транзакциях.
        Возвращает пустой список, если:
        - файл не найден
        - произошла ошибка при чтении Excel
    """
    logger.debug(f"Начало загрузки транзакций из Excel файла: {file_path}")

    # Проверяем существование файла
    if not Path(file_path).exists():
        logger.warning(f"Файл не найден: {file_path}")
        return DEFAULT_RETURN_VALUE

    try:
        # Чтение Excel через pandas
        df = pd.read_excel(file_path, engine="openpyxl")

        # Преобразование DataFrame в список словарей
        transactions_raw = df.to_dict("records")

        # Преобразование типов для соответствия формату JSON (числа могут быть float)
        transactions: List[Dict[str, Any]] = []
        for transaction_raw in transactions_raw:
            transaction: Dict[str, Any] = {}
            for key, value in transaction_raw.items():
                # Пропускаем NaN значения
                if isna(value):
                    continue
                # Преобразуем float в int для id, если возможно
                if key == "id" and isinstance(value, float):
                    transaction[key] = int(value)
                # Преобразуем float в str для amount, если нужно
                elif key == "amount" and isinstance(value, float):
                    transaction[key] = str(value)
                else:
                    transaction[key] = value
            transactions.append(transaction)

        logger.info(f"Успешно загружено {len(transactions)} транзакций из Excel файла: {file_path}")
        return transactions

    except pd.errors.EmptyDataError:
        logger.warning(f"Excel файл пустой: {file_path}")
        return DEFAULT_RETURN_VALUE
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла {file_path}: {type(e).__name__} - {e}")
        return DEFAULT_RETURN_VALUE

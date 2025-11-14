import os
from typing import Any, Dict

import requests  # type: ignore
from dotenv import load_dotenv  # type: ignore


def convert_currency_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными транзакции, содержащий:
            - operationAmount.amount: сумма транзакции (строка или число)
            - operationAmount.currency.code: код валюты (RUB, USD, EUR)

    Returns:
        Сумма транзакции в рублях (float).

    Raises:
        KeyError: Если в транзакции отсутствуют необходимые поля.
        ValueError: Если не удалось преобразовать сумму в число или конвертировать валюту.
        requests.RequestException: Если произошла ошибка при запросе к API.
    """
    # Загружаем переменные окружения
    load_dotenv()

    # Получаем API ключ из переменной окружения
    api_key = os.getenv("API_KEY_CURRENCY")
    if api_key is None:
        raise ValueError("API_KEY_CURRENCY не установлен в переменных окружения")

    # Извлекаем данные из транзакции
    if "operationAmount" not in transaction:
        raise KeyError("В транзакции отсутствует поле 'operationAmount'")

    operation_amount = transaction["operationAmount"]

    if "amount" not in operation_amount:
        raise KeyError("В транзакции отсутствует поле 'operationAmount.amount'")

    if "currency" not in operation_amount:
        raise KeyError("В транзакции отсутствует поле 'operationAmount.currency'")

    currency_data = operation_amount["currency"]

    if not isinstance(currency_data, dict):
        raise ValueError("Поле 'operationAmount.currency' должно быть словарем")

    if "code" not in currency_data:
        raise KeyError("В транзакции отсутствует поле 'operationAmount.currency.code'")

    amount_str = operation_amount["amount"]
    currency_code = currency_data["code"]

    # Преобразуем сумму в число
    try:
        amount = float(amount_str)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Не удалось преобразовать сумму '{amount_str}' в число: {e}") from e

    # Если валюта уже в рублях, возвращаем сумму как есть
    if currency_code == "RUB":
        return amount

    # Если валюта USD или EUR, делаем запрос к API
    if currency_code not in ("USD", "EUR"):
        raise ValueError(f"Неподдерживаемая валюта: {currency_code}. Поддерживаются только RUB, USD, EUR")

    # Формируем URL для API запроса
    api_url = "https://api.apilayer.com/exchangerates_data/convert"

    # Параметры запроса
    params = {
        "from": currency_code,
        "to": "RUB",
        "amount": amount,
    }

    # Заголовки с API ключом
    headers = {
        "apikey": api_key,
    }

    try:
        # Выполняем GET запрос к API
        response = requests.get(api_url, params=params, headers=headers, timeout=10)

        # Проверяем статус ответа
        response.raise_for_status()

        # Парсим JSON ответ
        response_data = response.json()

        # Проверяем наличие поля result в ответе
        if "result" not in response_data:
            raise ValueError(f"В ответе API отсутствует поле 'result'. Ответ: {response_data}")

        # Извлекаем конвертированную сумму
        converted_amount = response_data["result"]

        # Преобразуем в float и возвращаем
        return float(converted_amount)

    except requests.RequestException as e:
        raise requests.RequestException(f"Ошибка при запросе к API конвертации валют: {e}") from e

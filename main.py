from generators import (card_number_generator, filter_by_currency, random_card_number_generator,
                        transaction_descriptions)
from src.decorators import log
from src.external_api import convert_currency_to_rubles
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions_from_json
from src.widget import get_date, mask_account_card


def demo() -> None:
    """Демонстрация работы масок для карт и счетов с обработкой ошибок."""

    # Примеры номеров карт
    card_16 = 1234567890123456  # 16 цифр → формат: XXXX XX** **** XXXX
    card_19 = "1234567890123456789"  # 19 цифр → первые 6 и последние 4, середина — '*'
    card_bad = "1234abcd"  # Нецифровые символы → ошибка

    # Примеры номеров счетов
    acc_normal = 123456789
    acc_short = 321  # Менее 4 цифр → показываем всё, но с префиксом '**'

    print("Маскирование карт:")
    test_cards: list[int | str] = [card_16, card_19, card_bad]
    for cn in test_cards:
        try:
            print(f"  {cn} -> {get_mask_card_number(cn)}")
        except ValueError as err:
            print(f"  Ошибка для '{cn}': {err}")

    print("\nМаскирование счетов:")
    for an in [acc_normal, acc_short]:
        try:
            print(f"  {an} -> {get_mask_account(an)}")
        except ValueError as err:
            print(f"  Ошибка для '{an}': {err}")

    print("\n" + "=" * 60)
    print("Демонстрация новой функции mask_account_card:")
    print("=" * 60)

    # Примеры для новой функции
    test_strings = [
        "Visa Platinum 7000792289606361",
        "Maestro 7000792289606361",
        "Mastercard 5555555555554444",
        "Счет 73654108430135874305",
        "Счет 1234 5678 9012 3456",
        "American Express 378282246310005",
    ]

    for test_string in test_strings:
        try:
            result = mask_account_card(test_string)
            print(f"  {test_string}")
            print(f"  -> {result}")
            print()
        except ValueError as err:
            print(f"  Ошибка для '{test_string}': {err}")
            print()

    print("\n" + "=" * 60)
    print("Демонстрация функции get_date:")
    print("=" * 60)

    # Примеры для функции get_date
    test_dates = [
        "2024-03-11T02:26:18.671407",
        "2023-12-25T15:30:45.123456",
        "2024-01-01T00:00:00",
        "2024-02-29T12:00:00.000000",
        "неверная дата",
    ]

    for test_date in test_dates:
        try:
            result = get_date(test_date)
            print(f"  {test_date}")
            print(f"  -> {result}")
            print()
        except ValueError as err:
            print(f"  Ошибка для '{test_date}': {err}")
            print()

    print("\n" + "=" * 60)
    print("Демонстрация функций из processing.py:")
    print("=" * 60)

    # Примеры для функций filter_by_state и sort_by_date
    sample_transactions: list[dict[str, object]] = [
        {"id": 1, "state": "EXECUTED", "date": "2023-12-25T15:30:45.123456", "amount": 100.0},
        {"id": 2, "state": "PENDING", "date": "2023-12-26T10:15:30.654321", "amount": 200.0},
        {"id": 3, "state": "EXECUTED", "date": "2023-12-24T18:45:12.987654", "amount": 150.0},
        {"id": 4, "state": "CANCELED", "date": "2023-12-27T09:20:05.555555", "amount": 300.0},
        {"id": 5, "state": "EXECUTED", "date": "2023-12-23T22:10:33.777777", "amount": 250.0},
    ]

    print("\nДемонстрация filter_by_state:")
    print("\nИсходные транзакции:")
    for tx in sample_transactions:
        print(f"  ID: {tx['id']}, Состояние: {tx['state']}, Дата: {get_date(str(tx['date']))}, Сумма: {tx['amount']}")

    filtered_transactions = filter_by_state(sample_transactions)
    print("\nОтфильтрованные транзакции (только EXECUTED):")
    for tx in filtered_transactions:
        print(f"  ID: {tx['id']}, Состояние: {tx['state']}, Дата: {get_date(str(tx['date']))}, Сумма: {tx['amount']}")

    print("\nДемонстрация sort_by_date:")
    sorted_transactions = sort_by_date(sample_transactions)
    print("\nТранзакции, отсортированные по дате (от новых к старым):")
    for tx in sorted_transactions:
        print(f"  ID: {tx['id']}, Состояние: {tx['state']}, Дата: {get_date(str(tx['date']))}, Сумма: {tx['amount']}")

    print("\nТранзакции, отсортированные по дате (от старых к новым):")
    sorted_asc = sort_by_date(sample_transactions, is_reverse_order=False)
    for tx in sorted_asc:
        print(f"  ID: {tx['id']}, Состояние: {tx['state']}, Дата: {get_date(str(tx['date']))}, Сумма: {tx['amount']}")


def demo_generators() -> None:
    """Демонстрация работы функций из модуля generators."""

    print("\n" + "=" * 60)
    print("Демонстрация функций из generators.py:")
    print("=" * 60)

    # Примеры транзакций для демонстрации
    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]

    # Демонстрация filter_by_currency
    print("\nДемонстрация filter_by_currency:")
    print("\nФильтрация транзакций по USD:")
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    for transaction in usd_transactions:
        print(
            f"  ID: {transaction['id']}, Описание: {transaction['description']}, "
            f"Сумма: {transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['code']}"
        )

    print("\nФильтрация транзакций по RUB:")
    rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
    for transaction in rub_transactions:
        print(
            f"  ID: {transaction['id']}, Описание: {transaction['description']}, "
            f"Сумма: {transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['code']}"
        )

    # Демонстрация transaction_descriptions
    print("\nДемонстрация transaction_descriptions:")
    descriptions = list(transaction_descriptions(sample_transactions))
    print("\nОписания транзакций:")
    for i, description in enumerate(descriptions, 1):
        print(f"  {i}. {description}")

    # Демонстрация card_number_generator
    print("\nДемонстрация card_number_generator:")
    print("\nГенерация номеров карт в диапазоне от 1 до 5:")
    cards = list(card_number_generator(1, 5))
    for card in cards:
        print(f"  {card}")

    print("\nГенерация номеров карт в большом диапазоне:")
    cards_large = list(card_number_generator(1000, 1005))
    for card in cards_large:
        print(f"  {card}")

    # Демонстрация random_card_number_generator
    print("\nДемонстрация random_card_number_generator:")
    print("\nГенерация 5 случайных номеров карт:")
    random_cards = list(random_card_number_generator(5))
    for i, card in enumerate(random_cards, 1):
        print(f"  {i}. {card}")


def demo_log() -> None:
    """Демонстрация работы декоратора log."""

    print("\n" + "=" * 60)
    print("Демонстрация работы декоратора log:")
    print("=" * 60)

    # Демонстрация работы декоратора с логированием в файл
    @log()  # По умолчанию логи записываются в logfile.txt
    def add_numbers(a: int, b: int) -> int:
        """Складывает два числа."""
        return a + b

    @log()  # По умолчанию логи записываются в logfile.txt
    def divide_numbers(a: int, b: int) -> float:
        """Делит одно число на другое."""
        return a / b

    @log(filename=None)  # Логи выводятся в консоль
    def greet(name: str = "Гость") -> str:
        """Возвращает приветствие."""
        return f"Привет, {name}!"

    print("\nДемонстрация логирования в файл (logfile.txt):")
    result1 = add_numbers(5, 7)
    print(f"Результат сложения: {result1}")

    result2 = divide_numbers(10, 2)
    print(f"Результат деления: {result2}")

    print("\nДемонстрация логирования в консоль:")
    result3 = greet("Мир")
    print(f"Результат функции greet: {result3}")

    print("\nДемонстрация обработки ошибки:")
    try:
        result4 = divide_numbers(5, 0)  # Это вызовет ошибку
        print(f"Результат деления: {result4}")
    except ZeroDivisionError:
        print("Произошла ошибка деления на ноль (проверьте logfile.txt для просмотра лога ошибки)")

    print("\nПроверьте файл logfile.txt для просмотра логов выполнения функций")


def demo_utils_and_api() -> None:
    """Демонстрация работы функций из модулей utils и external_api."""

    print("\n" + "=" * 60)
    print("Демонстрация функций из utils.py и external_api.py:")
    print("=" * 60)

    # Демонстрация load_transactions_from_json
    print("\nДемонстрация load_transactions_from_json:")
    print("\nЗагрузка транзакций из файла data/operations.json:")

    transactions = load_transactions_from_json("data/operations.json")
    print(f"  ✅ Загружено транзакций: {len(transactions)}")

    if transactions:
        print("\n  Пример первой транзакции:")
        first_tx = transactions[0]
        print(f"    ID: {first_tx.get('id', 'N/A')}")
        print(f"    Дата: {first_tx.get('date', 'N/A')}")
        print(f"    Описание: {first_tx.get('description', 'N/A')}")
        if "operationAmount" in first_tx:
            amount = first_tx["operationAmount"].get("amount", "N/A")
            currency = first_tx["operationAmount"].get("currency", {}).get("code", "N/A")
            print(f"    Сумма: {amount} {currency}")

    print("\n  Проверка обработки несуществующего файла:")
    empty_result = load_transactions_from_json("nonexistent_file.json")
    print(f"    Несуществующий файл → {empty_result} (пустой список)")

    # Демонстрация convert_currency_to_rubles
    print("\n" + "=" * 60)
    print("Демонстрация convert_currency_to_rubles:")
    print("=" * 60)

    # Пример с RUB (не требует API)
    print("\nКонвертация транзакции в RUB (не требует API):")
    rub_transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "RUB", "name": "руб."},
        },
        "description": "Тестовая транзакция в рублях",
    }

    try:
        import os
        from unittest.mock import patch

        # Устанавливаем тестовый API ключ для демонстрации
        with patch.dict(os.environ, {"API_KEY_CURRENCY": "demo_key"}):  # type: ignore
            result = convert_currency_to_rubles(rub_transaction)
            amount = rub_transaction.get("operationAmount", {}).get("amount", "N/A")  # type: ignore
            print(f"  Транзакция: {amount} RUB")
            print(f"  Результат: {result} RUB (сумма возвращается как есть)")
    except Exception as e:
        print(f"  ⚠️  Ошибка: {e}")

    # Примеры с USD и EUR (требуют API, но покажем структуру)
    print("\nКонвертация транзакций в USD и EUR (требуют API ключ):")
    print("  ⚠️  Для работы с USD/EUR необходим API_KEY_CURRENCY в .env")
    print("  ⚠️  Получить ключ можно на: https://apilayer.com/exchangerates_data-api")

    usd_transaction = {
        "operationAmount": {
            "amount": "100.0",
            "currency": {"code": "USD", "name": "USD"},
        },
        "description": "Тестовая транзакция в долларах",
    }

    eur_transaction = {
        "operationAmount": {
            "amount": "50.0",
            "currency": {"code": "EUR", "name": "EUR"},
        },
        "description": "Тестовая транзакция в евро",
    }

    print("\n  Пример транзакции в USD:")
    usd_amount = usd_transaction.get("operationAmount", {}).get("amount", "N/A")  # type: ignore
    print(f"    Транзакция: {usd_amount} USD")
    print("    → Требуется запрос к API для получения курса")

    print("\n  Пример транзакции в EUR:")
    eur_amount = eur_transaction.get("operationAmount", {}).get("amount", "N/A")  # type: ignore
    print(f"    Транзакция: {eur_amount} EUR")
    print("    → Требуется запрос к API для получения курса")

    # Демонстрация работы с реальными транзакциями из файла
    print("\n" + "=" * 60)
    print("Демонстрация работы с реальными транзакциями:")
    print("=" * 60)

    if transactions:
        print("\nПримеры транзакций из файла operations.json:")

        # Показываем первые 3 транзакции с разными валютами
        shown_count = 0
        for tx in transactions:
            if "operationAmount" in tx:
                amount = tx["operationAmount"].get("amount", "N/A")
                currency_code = tx["operationAmount"].get("currency", {}).get("code", "N/A")
                description = tx.get("description", "N/A")

                print(f"\n  Транзакция #{tx.get('id', 'N/A')}:")
                print(f"    Описание: {description}")
                print(f"    Сумма: {amount} {currency_code}")

                # Пытаемся конвертировать только RUB (без API)
                if currency_code == "RUB":
                    try:
                        import os
                        from unittest.mock import patch

                        with patch.dict(os.environ, {"API_KEY_CURRENCY": "demo_key"}):  # type: ignore
                            result = convert_currency_to_rubles(tx)
                            print(f"    В рублях: {result} RUB")
                    except Exception:
                        pass
                else:
                    print(f"    → Для конвертации {currency_code} требуется API ключ")

                shown_count += 1
                if shown_count >= 3:
                    break

    print("\n" + "=" * 60)
    print("Примечание:")
    print("=" * 60)
    print("Для полной работы с конвертацией валют:")
    print("1. Получите API ключ на https://apilayer.com/exchangerates_data-api")
    print("2. Создайте файл .env в корне проекта")
    print("3. Добавьте в .env: API_KEY_CURRENCY=ваш_ключ")


if __name__ == "__main__":
    demo()
    demo_generators()
    demo_log()
    demo_utils_and_api()

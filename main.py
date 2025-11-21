from typing import Any, Dict, List

from src.csv_loader import load_transactions_from_csv, load_transactions_from_excel
from src.processing import filter_by_currency, filter_by_state, process_bank_search, sort_by_date
from src.utils import load_transactions_from_json
from src.widget import get_date, mask_account_card


def main() -> None:
    """
    Основная функция программы для работы с банковскими транзакциями.

    Предоставляет пользовательский интерфейс для:
    - Загрузки транзакций из файлов (JSON, CSV, XLSX)
    - Фильтрации по статусу
    - Сортировки по дате
    - Фильтрации по валюте
    - Поиска по описанию
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор типа файла
    file_choice = input().strip()

    transactions: List[Dict[str, Any]] = []

    if file_choice == "1":
        print("Для обработки выбран JSON-файл.")
        transactions = load_transactions_from_json("data/operations.json")
    elif file_choice == "2":
        print("Для обработки выбран CSV-файл.")
        transactions = load_transactions_from_csv("data/transactions.csv")
    elif file_choice == "3":
        print("Для обработки выбран XLSX-файл.")
        transactions = load_transactions_from_excel("data/transactions_excel.xlsx")
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Выбор статуса операций
    valid_states = ["EXECUTED", "CANCELED", "PENDING"]
    state = None

    while state not in valid_states:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_states)}")
        user_input = input().strip().upper()

        if user_input in valid_states:
            state = user_input
        else:
            print(f'Статус операции "{user_input}" недоступен.')

    # Фильтрация по статусу
    transactions = filter_by_state(transactions, state)
    print(f'Операции отфильтрованы по статусу "{state}"')

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    print("Отсортировать операции по дате? Да/Нет")
    sort_choice = input().strip().lower()

    if sort_choice in ["да", "yes", "y"]:
        print("Отсортировать по возрастанию или по убыванию?")
        order_choice = input().strip().lower()

        is_reverse = order_choice not in ["по возрастанию", "возрастанию", "возрастание"]
        transactions = sort_by_date(transactions, is_reverse_order=is_reverse)

    # Фильтрация по валюте
    print("Отфильтровать транзакции по валюте? Да/Нет")
    currency_choice = input().strip().lower()

    if currency_choice in ["да", "yes", "y"]:
        valid_currencies = {
            "1": "RUB",
            "2": "USD",
            "3": "EUR",
            "4": "другие",
        }
        currency_code = None

        while currency_code is None:
            print("Выберите валюту для фильтрации:")
            print("1. Рубль (RUB)")
            print("2. Доллар (USD)")
            print("3. Евро (EUR)")
            print("4. Другие валюты")
            user_currency_choice = input().strip()

            if user_currency_choice in valid_currencies:
                selected_currency = valid_currencies[user_currency_choice]

                if selected_currency == "другие":
                    # Получаем все уникальные валюты из транзакций
                    available_currencies = set()
                    for tx in transactions:
                        currency = tx.get("operationAmount", {}).get("currency", {}).get("code", "")
                        if currency and currency not in ["RUB", "USD", "EUR"]:
                            available_currencies.add(currency)

                    if available_currencies:
                        print(f"Доступные другие валюты: {', '.join(sorted(available_currencies))}")
                        print("Введите код валюты:")
                        user_currency_code = input().strip().upper()

                        if user_currency_code in available_currencies:
                            currency_code = user_currency_code
                        else:
                            print(f'Валюта "{user_currency_code}" не найдена в транзакциях.')
                    else:
                        print("Других валют не найдено в транзакциях.")
                        break
                else:
                    currency_code = selected_currency
            else:
                print(f'Неверный выбор "{user_currency_choice}". Выберите от 1 до 4.')

        if currency_code:
            transactions = filter_by_currency(transactions, currency_code)
            currency_name = {"RUB": "рублевые", "USD": "долларовые", "EUR": "евро"}.get(currency_code, currency_code)
            print(f"Операции отфильтрованы по {currency_name} транзакциям")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Фильтрация по слову в описании
    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    search_choice = input().strip().lower()

    if search_choice in ["да", "yes", "y"]:
        print("Введите слово для поиска:")
        search_word = input().strip()

        if search_word:
            transactions = process_bank_search(transactions, search_word)

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Вывод результатов
    print("Распечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        # Форматирование даты
        date_str = get_date(transaction.get("date", ""))

        # Форматирование описания
        description = transaction.get("description", "")

        # Форматирование суммы
        amount = transaction.get("operationAmount", {}).get("amount", "")
        currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("name", "")

        # Форматирование отправителя и получателя
        from_str = transaction.get("from", "")
        to_str = transaction.get("to", "")

        # Вывод транзакции
        print(f"{date_str} {description}")

        if from_str:
            masked_from = mask_account_card(from_str)
            if to_str:
                masked_to = mask_account_card(to_str)
                print(f"{masked_from} -> {masked_to}")
            else:
                print(f"Счет **{from_str[-4:]}")
        elif to_str:
            print(f"Счет **{to_str[-4:]}")

        print(f"Сумма: {amount} {currency_name}\n")


if __name__ == "__main__":
    main()

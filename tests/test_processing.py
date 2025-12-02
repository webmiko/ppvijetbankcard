from typing import Any

from src.processing import (
    filter_by_currency,
    filter_by_state,
    process_bank_operations,
    process_bank_search,
    sort_by_date,
)


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    def test_filter_by_state_default(self) -> None:
        """Проверка фильтрации по состоянию EXECUTED (по умолчанию)."""
        transactions = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "PENDING"},
            {"id": 3, "state": "EXECUTED"},
            {"id": 4, "state": "CANCELED"},
        ]
        result = filter_by_state(transactions)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3

    def test_filter_by_state_custom(self) -> None:
        """Проверка фильтрации по пользовательскому состоянию."""
        transactions = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "PENDING"},
            {"id": 3, "state": "PENDING"},
            {"id": 4, "state": "CANCELED"},
        ]
        result = filter_by_state(transactions, "PENDING")
        assert len(result) == 2
        assert result[0]["id"] == 2
        assert result[1]["id"] == 3

    def test_filter_by_state_empty(self) -> None:
        """Проверка фильтрации пустого списка."""
        assert filter_by_state([]) == []

    def test_filter_by_state_no_match(self) -> None:
        """Проверка фильтрации без совпадений."""
        transactions = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "EXECUTED"}]
        result = filter_by_state(transactions, "PENDING")
        assert result == []

    def test_filter_by_state_missing_state_key(self) -> None:
        """Проверка обработки транзакций без ключа state."""
        transactions: list[dict[str, Any]] = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2},  # Без ключа state
            {"id": 3, "state": "EXECUTED"},
        ]
        result = filter_by_state(transactions)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_sort_by_date_descending(self) -> None:
        """Проверка сортировки по убыванию (по умолчанию)."""
        transactions = [
            {"id": 1, "date": "2023-03-11T02:26:18.671407"},
            {"id": 2, "date": "2023-04-15T10:30:00.123456"},
            {"id": 3, "date": "2023-02-05T18:45:30.987654"},
        ]
        result = sort_by_date(transactions)
        assert result[0]["id"] == 2  # Апрель
        assert result[1]["id"] == 1  # Март
        assert result[2]["id"] == 3  # Февраль

    def test_sort_by_date_ascending(self) -> None:
        """Проверка сортировки по возрастанию."""
        transactions = [
            {"id": 1, "date": "2023-03-11T02:26:18.671407"},
            {"id": 2, "date": "2023-04-15T10:30:00.123456"},
            {"id": 3, "date": "2023-02-05T18:45:30.987654"},
        ]
        result = sort_by_date(transactions, is_reverse_order=False)
        assert result[0]["id"] == 3  # Февраль
        assert result[1]["id"] == 1  # Март
        assert result[2]["id"] == 2  # Апрель

    def test_sort_by_date_empty(self) -> None:
        """Проверка сортировки пустого списка."""
        assert sort_by_date([]) == []

    def test_sort_by_date_same_dates(self) -> None:
        """Проверка сортировки с одинаковыми датами."""
        base_date = "2023-03-11T02:26:18.671407"
        transactions = [{"id": 1, "date": base_date}, {"id": 2, "date": base_date}, {"id": 3, "date": base_date}]
        result = sort_by_date(transactions)
        assert len(result) == 3
        # Порядок должен сохраниться при одинаковых датах
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2
        assert result[2]["id"] == 3


class TestProcessBankSearch:
    """Тесты для функции process_bank_search."""

    def test_process_bank_search_success(self) -> None:
        """Тест успешного поиска транзакций."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Открытие вклада"},
            {"id": 3, "description": "Перевод со счета на счет"},
        ]

        result = process_bank_search(transactions, "Перевод")

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3

    def test_process_bank_search_case_insensitive(self) -> None:
        """Тест регистронезависимого поиска."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "ОТКРЫТИЕ ВКЛАДА"},
        ]

        result = process_bank_search(transactions, "открытие")

        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_process_bank_search_empty_list(self) -> None:
        """Тест поиска с пустым списком транзакций."""
        transactions: list[dict[str, Any]] = []

        result = process_bank_search(transactions, "Перевод")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_process_bank_search_empty_string(self) -> None:
        """Тест поиска с пустой строкой поиска."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
        ]

        result = process_bank_search(transactions, "")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_process_bank_search_not_found(self) -> None:
        """Тест поиска, когда ничего не найдено."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
        ]

        result = process_bank_search(transactions, "Несуществующий текст")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_process_bank_search_special_characters(self) -> None:
        """Тест поиска с специальными символами в строке поиска."""
        transactions = [
            {"id": 1, "description": "Перевод (организация)"},
            {"id": 2, "description": "Открытие вклада"},
        ]

        result = process_bank_search(transactions, "Перевод (организация)")

        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_process_bank_search_missing_description(self) -> None:
        """Тест поиска с транзакциями без поля description."""
        transactions: list[dict[str, Any]] = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2},  # Без поля description
            {"id": 3, "description": "Перевод со счета"},
        ]

        result = process_bank_search(transactions, "Перевод")

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3

    def test_process_bank_search_attribute_error(self) -> None:
        """Тест обработки AttributeError при некорректных данных транзакции."""
        transactions: list[dict[str, Any] | None] = [
            {"id": 1, "description": "Перевод организации"},
            None,  # None вместо словаря
            {"id": 3, "description": "Перевод со счета"},
        ]

        result = process_bank_search(transactions, "Перевод")  # type: ignore[arg-type]

        assert isinstance(result, list)
        assert len(result) == 0
        assert result == []

    def test_process_bank_search_type_error(self) -> None:
        """Тест обработки TypeError при некорректном типе description."""
        transactions: list[dict[str, Any]] = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": 12345},  # Не строка
            {"id": 3, "description": "Перевод со счета"},
        ]

        result = process_bank_search(transactions, "Перевод")

        assert isinstance(result, list)
        assert len(result) == 0
        assert result == []

    def test_process_bank_search_partial_match(self) -> None:
        """Тест поиска частичного совпадения в описании."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Перевод со счета на счет"},
            {"id": 3, "description": "Открытие вклада"},
        ]

        result = process_bank_search(transactions, "Перевод")

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    def test_process_bank_search_multiple_matches(self) -> None:
        """Тест поиска с множественными совпадениями в одной транзакции."""
        transactions = [
            {"id": 1, "description": "Перевод организации Перевод средств"},
            {"id": 2, "description": "Открытие вклада"},
        ]

        result = process_bank_search(transactions, "Перевод")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == 1


class TestProcessBankOperations:
    """Тесты для функции process_bank_operations."""

    def test_process_bank_operations_success(self) -> None:
        """Тест успешного подсчета операций."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Открытие вклада"},
            {"id": 3, "description": "Перевод организации"},
            {"id": 4, "description": "Перевод со счета на счет"},
        ]
        categories = ["Перевод организации", "Открытие вклада"]

        result = process_bank_operations(transactions, categories)

        assert isinstance(result, dict)
        assert result["Перевод организации"] == 2
        assert result["Открытие вклада"] == 1

    def test_process_bank_operations_empty_list(self) -> None:
        """Тест подсчета с пустым списком транзакций."""
        transactions: list[dict[str, Any]] = []
        categories = ["Перевод организации"]

        result = process_bank_operations(transactions, categories)

        assert isinstance(result, dict)
        assert len(result) == 0
        assert result == {}

    def test_process_bank_operations_empty_categories(self) -> None:
        """Тест подсчета с пустым списком категорий."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
        ]
        categories: list[str] = []

        result = process_bank_operations(transactions, categories)

        assert isinstance(result, dict)
        assert len(result) == 0

    def test_process_bank_operations_category_not_found(self) -> None:
        """Тест подсчета, когда категория не найдена."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
        ]
        categories = ["Несуществующая категория"]

        result = process_bank_operations(transactions, categories)

        assert isinstance(result, dict)
        assert result["Несуществующая категория"] == 0

    def test_process_bank_operations_multiple_categories(self) -> None:
        """Тест подсчета нескольких категорий."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Открытие вклада"},
            {"id": 3, "description": "Перевод организации"},
            {"id": 4, "description": "Перевод со счета на счет"},
            {"id": 5, "description": "Открытие вклада"},
            {"id": 6, "description": "Открытие вклада"},
        ]
        categories = ["Перевод организации", "Открытие вклада", "Перевод со счета на счет"]

        result = process_bank_operations(transactions, categories)

        assert isinstance(result, dict)
        assert result["Перевод организации"] == 2
        assert result["Открытие вклада"] == 3
        assert result["Перевод со счета на счет"] == 1

    def test_process_bank_operations_missing_description(self) -> None:
        """Тест подсчета с транзакциями без поля description."""
        transactions: list[dict[str, Any]] = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2},  # Без поля description
            {"id": 3, "description": "Перевод организации"},
        ]
        categories = ["Перевод организации"]

        result = process_bank_operations(transactions, categories)

        assert isinstance(result, dict)
        assert result["Перевод организации"] == 2

    def test_process_bank_operations_attribute_error(self) -> None:
        """Тест обработки AttributeError при некорректных данных транзакции."""
        transactions: list[dict[str, Any] | None] = [
            {"id": 1, "description": "Перевод организации"},
            None,  # None вместо словаря
            {"id": 3, "description": "Перевод организации"},
        ]
        categories = ["Перевод организации"]

        result = process_bank_operations(transactions, categories)  # type: ignore[arg-type]

        assert isinstance(result, dict)
        assert len(result) == 0
        assert result == {}

    def test_process_bank_operations_type_error(self) -> None:
        """Тест обработки TypeError при некорректном типе description."""
        transactions: list[dict[str, Any]] = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": 12345},  # Не строка
            {"id": 3, "description": "Перевод организации"},
        ]
        categories = ["Перевод организации"]

        result = process_bank_operations(transactions, categories)

        assert isinstance(result, dict)
        assert result["Перевод организации"] == 2

    def test_process_bank_operations_duplicate_categories(self) -> None:
        """Тест подсчета с дублирующимися категориями в списке."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Открытие вклада"},
        ]
        categories = ["Перевод организации", "Перевод организации", "Открытие вклада"]

        result = process_bank_operations(transactions, categories)

        assert isinstance(result, dict)
        assert result["Перевод организации"] == 1
        assert result["Открытие вклада"] == 1

    def test_process_bank_operations_all_categories_zero(self) -> None:
        """Тест подсчета, когда все категории имеют нулевое значение."""
        transactions = [
            {"id": 1, "description": "Другая операция"},
            {"id": 2, "description": "Еще одна операция"},
        ]
        categories = ["Перевод организации", "Открытие вклада"]

        result = process_bank_operations(transactions, categories)

        assert isinstance(result, dict)
        assert result["Перевод организации"] == 0
        assert result["Открытие вклада"] == 0


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_by_currency_success(self) -> None:
        """Тест успешной фильтрации по валюте."""
        transactions = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
            {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}},
        ]

        result = filter_by_currency(transactions, "RUB")

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3

    def test_filter_by_currency_empty_list(self) -> None:
        """Тест фильтрации с пустым списком транзакций."""
        transactions: list[dict[str, Any]] = []

        result = filter_by_currency(transactions, "RUB")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_filter_by_currency_empty_code(self) -> None:
        """Тест фильтрации с пустым кодом валюты."""
        transactions = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
        ]

        result = filter_by_currency(transactions, "")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_filter_by_currency_not_found(self) -> None:
        """Тест фильтрации, когда валюта не найдена."""
        transactions = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
        ]

        result = filter_by_currency(transactions, "EUR")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_filter_by_currency_missing_operation_amount(self) -> None:
        """Тест фильтрации с транзакциями без поля operationAmount."""
        transactions: list[dict[str, Any]] = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 2},  # Без поля operationAmount
            {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}},
        ]

        result = filter_by_currency(transactions, "RUB")

        assert isinstance(result, list)
        assert len(result) == 2

    def test_filter_by_currency_missing_currency(self) -> None:
        """Тест фильтрации с транзакциями без поля currency."""
        transactions: list[dict[str, Any]] = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 2, "operationAmount": {}},  # Без поля currency
            {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}},
        ]

        result = filter_by_currency(transactions, "RUB")

        assert isinstance(result, list)
        assert len(result) == 2

    def test_filter_by_currency_missing_code(self) -> None:
        """Тест фильтрации с транзакциями без поля code."""
        transactions: list[dict[str, Any]] = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 2, "operationAmount": {"currency": {}}},  # Без поля code
            {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}},
        ]

        result = filter_by_currency(transactions, "RUB")

        assert isinstance(result, list)
        assert len(result) == 2

    def test_filter_by_currency_attribute_error(self) -> None:
        """Тест обработки AttributeError при некорректных данных транзакции."""
        transactions: list[dict[str, Any] | None] = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            None,  # None вместо словаря
            {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}},
        ]

        result = filter_by_currency(transactions, "RUB")  # type: ignore[arg-type]

        assert isinstance(result, list)
        assert len(result) == 0
        assert result == []

    def test_filter_by_currency_type_error(self) -> None:
        """Тест обработки TypeError при некорректном типе данных."""
        transactions: list[dict[str, Any]] = [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 2, "operationAmount": "invalid"},  # Не словарь
            {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}},
        ]

        result = filter_by_currency(transactions, "RUB")

        assert isinstance(result, list)
        assert len(result) == 0
        assert result == []

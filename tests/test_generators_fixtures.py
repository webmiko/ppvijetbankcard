import pytest

from generators.generators import card_number_generator, filter_by_currency, transaction_descriptions

# Тестовые данные
transactions = [
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


# Параметризованные тесты для filter_by_currency
@pytest.mark.parametrize(
    "currency_code, expected_count",
    [
        ("USD", 2),
        ("RUB", 1),
        ("EUR", 0),
    ],
)
def test_filter_by_currency_parametrized(currency_code: str, expected_count: int) -> None:
    """Проверка фильтрации транзакций по различным валютам."""
    filtered_transactions = list(filter_by_currency(transactions, currency_code))
    assert len(filtered_transactions) == expected_count
    for transaction in filtered_transactions:
        assert transaction["operationAmount"]["currency"]["code"] == currency_code


# Параметризованные тесты для transaction_descriptions
@pytest.mark.parametrize(
    "index, expected_description",
    [
        (0, "Перевод организации"),
        (1, "Перевод со счета на счет"),
        (2, "Перевод со счета на счет"),
    ],
)
def test_transaction_descriptions_parametrized(index: int, expected_description: str) -> None:
    """Проверка получения описаний транзакций по индексу."""
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions[index] == expected_description


# Параметризованные тесты для card_number_generator
@pytest.mark.parametrize(
    "start, end, expected_first, expected_last",
    [
        (1, 3, "0000 0000 0000 0001", "0000 0000 0000 0003"),
        (100, 102, "0000 0000 0000 0100", "0000 0000 0000 0102"),
        (9999, 10001, "0000 0000 0000 9999", "0000 0000 0001 0001"),
    ],
)
def test_card_number_generator_parametrized(start: int, end: int, expected_first: str, expected_last: str) -> None:
    """Проверка генерации номеров карт в различных диапазонах."""
    cards = list(card_number_generator(start, end))
    assert len(cards) == end - start + 1
    assert cards[0] == expected_first
    assert cards[-1] == expected_last

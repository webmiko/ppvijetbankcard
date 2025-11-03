from generators.generators import (card_number_generator, filter_by_currency, random_card_number_generator,
                                   transaction_descriptions)

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
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


# Тесты для filter_by_currency
def test_filter_by_currency_usd() -> None:
    """Проверка фильтрации транзакций по USD."""
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 3
    for transaction in usd_transactions:
        assert transaction["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_rub() -> None:
    """Проверка фильтрации транзакций по RUB."""
    rub_transactions = list(filter_by_currency(transactions, "RUB"))
    assert len(rub_transactions) == 2
    for transaction in rub_transactions:
        assert transaction["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_empty() -> None:
    """Проверка фильтрации транзакций по отсутствующей валюте."""
    empty_transactions = list(filter_by_currency(transactions, "EUR"))
    assert len(empty_transactions) == 0


def test_filter_by_currency_empty_list() -> None:
    """Проверка фильтрации пустого списка транзакций."""
    empty_transactions = list(filter_by_currency([], "USD"))
    assert len(empty_transactions) == 0


# Тесты для transaction_descriptions
def test_transaction_descriptions() -> None:
    """Проверка получения описаний транзакций."""
    descriptions = list(transaction_descriptions(transactions))
    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert descriptions == expected_descriptions


def test_transaction_descriptions_empty() -> None:
    """Проверка получения описаний из пустого списка."""
    descriptions = list(transaction_descriptions([]))
    assert descriptions == []


# Тесты для card_number_generator
def test_card_number_generator() -> None:
    """Проверка генерации номеров карт."""
    cards = list(card_number_generator(1, 5))
    expected_cards = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    assert cards == expected_cards


def test_card_number_generator_single() -> None:
    """Проверка генерации одного номера карты."""
    cards = list(card_number_generator(10, 10))
    assert cards == ["0000 0000 0000 0010"]


def test_card_number_generator_large() -> None:
    """Проверка генерации больших номеров карт."""
    cards = list(card_number_generator(0, 2))
    expected_cards = ["0000 0000 0000 0000", "0000 0000 0000 0001", "0000 0000 0000 0002"]
    assert cards == expected_cards


# Тесты для random_card_number_generator
def test_random_card_number_generator() -> None:
    """Проверка генерации случайных номеров карт."""
    cards = list(random_card_number_generator(5))
    assert len(cards) == 5
    for card in cards:
        # Проверяем формат XXXX XXXX XXXX XXXX
        assert len(card) == 19  # 16 цифр + 3 пробела
        assert card[4] == " " and card[9] == " " and card[14] == " "
        # Проверяем, что все символы кроме пробелов - цифры
        for i, ch in enumerate(card):
            if i not in [4, 9, 14]:
                assert ch.isdigit()


def test_random_card_number_generator_single() -> None:
    """Проверка генерации одного случайного номера карты."""
    cards = list(random_card_number_generator(1))
    assert len(cards) == 1
    # Проверяем формат XXXX XXXX XXXX XXXX
    assert len(cards[0]) == 19  # 16 цифр + 3 пробела
    assert cards[0][4] == " " and cards[0][9] == " " and cards[0][14] == " "


def test_random_card_number_generator_empty() -> None:
    """Проверка генерации нулевого количества номеров карт."""
    cards = list(random_card_number_generator(0))
    assert len(cards) == 0

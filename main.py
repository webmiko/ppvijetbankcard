from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card, get_date


def demo() -> None:
    """Демонстрация работы масок для карт и счетов с обработкой ошибок."""

    # Примеры номеров карт
    card_16 = 1234567890123456            # 16 цифр → формат: XXXX XX** **** XXXX
    card_19 = "1234567890123456789"       # 19 цифр → первые 6 и последние 4, середина — '*'
    card_bad = "1234abcd"                 # Нецифровые символы → ошибка

    # Примеры номеров счетов
    acc_normal = 123456789
    acc_short = 321                        # Менее 4 цифр → показываем всё, но с префиксом '**'

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
        "American Express 378282246310005"
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
        "неверная дата"
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


if __name__ == "__main__":
    demo()

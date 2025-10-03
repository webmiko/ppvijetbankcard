from src.masks import get_mask_account, get_mask_card_number


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


if __name__ == "__main__":
    demo()

# Часто задаваемые вопросы (FAQ)

В этом разделе собраны ответы на часто задаваемые вопросы о библиотеке PPVijetBankCard.

## Общие вопросы

### Что такое PPVijetBankCard?

PPVijetBankCard - это библиотека Python для безопасной маскировки номеров банковских карт и счетов. Она предоставляет удобные функции для скрытия конфиденциальной информации о банковских картах и счетах, оставляя видимыми только необходимые цифры для идентификации.

### Каковы основные возможности библиотеки?

- Маскировка номеров банковских карт (показывает первые 6 и последние 4 цифры)
- Маскировка номеров банковских счетов (показывает только последние 4 цифры)
- Форматирование дат из ISO формата в читаемый вид
- Обработка и фильтрация финансовых транзакций
- Генераторы для эффективной обработки больших объемов данных

### Какова лицензия проекта?

Проект распространяется под лицензией MIT. Это позволяет свободно использовать, модифицировать и распространять код в личных и коммерческих целях.

## Установка и настройка

### Как установить библиотеку?

```bash
# Скачайте проект
git clone <ссылка-на-репозиторий>
cd PPVijetBankCard

# Создайте виртуальное окружение
python -m venv venv

# Активируйте окружение
# Windows:
venv\Scriptsctivate
# macOS/Linux:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### Какие требования к системе?

- Python 3.8+ (рекомендуется Python 3.9+)
- Стандартные библиотеки Python: datetime, typing

## Использование функций

### Как замаскировать номер карты?

Используйте функцию `get_mask_card_number` из модуля `src.masks`:

```python
from src.masks import get_mask_card_number

card_number = 1234567890123456
masked_card = get_mask_card_number(card_number)
print(masked_card)  # Результат: 1234 56** **** 3456
```

### Как замаскировать номер счета?

Используйте функцию `get_mask_account` из модуля `src.masks`:

```python
from src.masks import get_mask_account

account_number = 73654108430135874305
masked_account = get_mask_account(account_number)
print(masked_account)  # Результат: **4305
```

### Как автоматически определить тип данных (карта или счет)?

Используйте функцию `mask_account_card` из модуля `src.widget`:

```python
from src.widget import mask_account_card

card_string = "Visa Platinum 7000792289606361"
masked_card = mask_account_card(card_string)
print(masked_card)  # Результат: Visa Platinum 7000 79** **** 6361

account_string = "Счет 73654108430135874305"
masked_account = mask_account_card(account_string)
print(masked_account)  # Результат: Счет **4305
```

### Как отформатировать дату?

Используйте функцию `get_date` из модуля `src.widget`:

```python
from src.widget import get_date

date_string = "2024-03-11T02:26:18.671407"
formatted_date = get_date(date_string)
print(formatted_date)  # Результат: 11.03.2024
```

### Как отфильтровать транзакции по состоянию?

Используйте функцию `filter_by_state` из модуля `src.processing`:

```python
from src.processing import filter_by_state

executed_transactions = filter_by_state(transactions, "EXECUTED")
```

### Как отсортировать транзакции по дате?

Используйте функцию `sort_by_date` из модуля `src.processing`:

```python
from src.processing import sort_by_date

sorted_transactions = sort_by_date(transactions)
```

### Как отфильтровать транзакции по валюте?

Используйте генератор `filter_by_currency` из модуля `generators`:

```python
from generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction["description"], transaction["operationAmount"]["amount"])
```

## Обработка ошибок

### Что делать, если функция возвращает ошибку "Неверный формат"?

Убедитесь, что вы передаете корректные данные:

- Для функций маскировки карт и счетов - только цифры
- Для функции форматирования даты - строку в формате ISO
- Для функции умной маскировки - строку с типом и номером

### Как обрабатывать отсутствующие данные в транзакциях?

Используйте безопасный доступ к ключам через метод `.get()`:

```python
# Вместо transaction["from"] используйте
from_account = transaction.get("from", "")

# Вместо transaction["date"] используйте
date = transaction.get("date", "")
```

## Расширенные возможности

### Как сгенерировать номера карт для тестирования?

Используйте генератор `card_number_generator` из модуля `generators`:

```python
from generators import card_number_generator

card_numbers = card_number_generator(1, 5)
for card_number in card_numbers:
    print(card_number)
# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```

### Как получить все описания транзакций?

Используйте генератор `transaction_descriptions` из модуля `generators`:

```python
from generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for description in descriptions:
    print(description)
```

## Тестирование

### Как запустить тесты?

```bash
# Запуск всех тестов
pytest

# Запуск тестов с выводом покрытия
pytest --cov=src

# Запуск конкретного тестового файла
pytest tests/test_masks.py
```

### Как проверить покрытие кода тестами?

```bash
# Запуск тестов с покрытием
coverage run -m pytest

# Генерация HTML-отчета
coverage html

# Просмотр отчета
open htmlcov/index.html
```

## Участие в проекте

### Как внести вклад в проект?

1. Ознакомьтесь с кодом проекта и его структурой
2. Изучите существующие тесты и их структуру
3. Создайте issue с описанием предлагаемых изменений
4. Создайте pull request с вашими изменениями
5. Убедитесь, что все тесты проходят и покрытие кода не снижается

### Как сообщить об ошибке?

Создайте issue в репозитории проекта с описанием:

- Ожидаемое поведение
- Фактическое поведение
- Шаги для воспроизведения ошибки
- Версия Python и операционной системы

### Как запросить новую функцию?

Создайте issue в репозитории проекта с описанием:

- Предлагаемая функция
- Сценарий использования
- Ожидаемый результат

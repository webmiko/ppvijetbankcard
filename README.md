# Маскировка номеров банковских карт и счетов

**Простая и удобная библиотека для безопасной маскировки номеров банковских карт и счетов в Python.**

Этот проект поможет вам скрыть конфиденциальную информацию о банковских картах и счетах, оставив видимыми только необходимые цифры для идентификации.

## Что умеет программа

### Маскировка банковских карт
- **Скрывает средние цифры** номера карты, оставляя видимыми первые 6 и последние 4 цифры
- **Поддерживает все типы карт**: Visa, Mastercard, Maestro, American Express и другие
- **Работает с номерами** от 13 до 19 цифр

**Пример:** `1234567890123456` → `1234 56** **** 3456`

### Маскировка банковских счетов
- **Показывает только последние 4 цифры** номера счета
- **Скрывает все остальные** цифры за символами `**`

**Пример:** `73654108430135874305` → `**4305`

### Форматирование дат
- **Преобразует даты** из технического формата в читаемый вид
- **Поддерживает ISO формат** с микросекундами

**Пример:** `2024-03-11T02:26:18.671407` → `11.03.2024`

### Универсальная обработка
- **Автоматически определяет** тип данных (карта или счет)
- **Работает со строками** содержащими название типа и номер
- **Обрабатывает ошибки** с понятными сообщениями

## Быстрый старт

### Требования
- **Python 3.8+** (рекомендуется Python 3.9+)

### Установка

```bash
# 1. Скачайте проект
git clone <ссылка-на-репозиторий>
cd PPVijetBankCard

# 2. Создайте виртуальное окружение
python -m venv venv

# 3. Активируйте окружение
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Установите зависимости
pip install -r requirements.txt
```

### Демонстрация
```bash
# Запустите демо-программу
python main.py
```

## Примеры использования

### Декоратор для логирования

```python
from src.decorators import log

# Логирование в файл по умолчанию (logfile.txt)
@log()
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)  # Запишет в logfile.txt: "add_numbers ok"

# Логирование в указанный файл
@log(filename="my_app.log")
def divide_numbers(a, b):
    return a / b

result = divide_numbers(10, 2)  # Запишет в my_app.log: "divide_numbers ok"

# Логирование в консоль
@log(filename=None)  # или @log(filename="")
def multiply_numbers(a, b):
    return a * b

result = multiply_numbers(4, 3)  # Выведет в консоль: "multiply_numbers ok"

# Обработка ошибок
@log(filename="errors.log")
def risky_operation(x):
    return 10 / x

try:
    result = risky_operation(0)  # Запишет в errors.log: "risky_operation error: ZeroDivisionError. Деление на ноль невозможно! Inputs: (0,), {}"
except ZeroDivisionError:
    pass
```

### Базовые функции

```python
from src.masks import get_mask_card_number, get_mask_account

# Маскировка номера карты
card_number = 1234567890123456
masked_card = get_mask_card_number(card_number)
print(masked_card)  # Результат: 1234 56** **** 3456

# Маскировка номера счета
account_number = 123456789
masked_account = get_mask_account(account_number)
print(masked_account)  # Результат: **6789
```

### Умные функции

```python
from src.widget import mask_account_card, get_date

# Автоматическая маскировка карт и счетов
card_string = "Visa Platinum 7000792289606361"
masked_card = mask_account_card(card_string)
print(masked_card)  # Результат: Visa Platinum 7000 79** **** 6361

account_string = "Счет 73654108430135874305"
masked_account = mask_account_card(account_string)
print(masked_account)  # Результат: Счет **4305

# Форматирование дат
date_string = "2024-03-11T02:26:18.671407"
formatted_date = get_date(date_string)
print(formatted_date)  # Результат: 11.03.2024
```

## Подробные примеры

### Функция `mask_account_card`

**Автоматически определяет тип данных и применяет нужную маскировку:**

```python
# Различные типы банковских карт
mask_account_card("Visa Platinum 7000792289606361")
# → "Visa Platinum 7000 79** **** 6361"

mask_account_card("Maestro 7000792289606361")
# → "Maestro 7000 79** **** 6361"

mask_account_card("Mastercard 5555555555554444")
# → "Mastercard 5555 55** **** 4444"

# Банковские счета
mask_account_card("Счет 73654108430135874305")
# → "Счет **4305"

mask_account_card("Счет 1234 5678 9012 3456")
# → "Счет **3456"
```

### Функция `get_date`

**Преобразует технические даты в читаемый формат:**

```python
# Различные форматы дат
get_date("2024-03-11T02:26:18.671407")
# → "11.03.2024"

get_date("2023-12-25T15:30:45.123456")
# → "25.12.2023"

get_date("2024-01-01T00:00:00")
# → "01.01.2024"

get_date("2024-02-29T12:00:00.000000")
# → "29.02.2024" (високосный год)
```

## Для разработчиков

### Инструменты качества кода

Проект использует современные инструменты для обеспечения качества:

- **Black** - автоматическое форматирование кода
- **Flake8** - проверка стиля и ошибок
- **isort** - сортировка импортов
- **mypy** - статическая проверка типов

### Команды для разработки

```bash
# Форматирование кода
black .

# Проверка стиля
flake8 .

# Сортировка импортов
isort .

# Проверка типов
mypy .
```

### Тестирование

Проект имеет комплексный набор тестов для проверки корректности работы всех функций:

```bash
# Запуск всех тестов
pytest

# Запуск тестов с выводом покрытия
pytest --cov=src

# Запуск конкретного тестового файла
pytest tests/test_masks.py

# Запуск тестов с генерацией HTML-отчета о покрытии
coverage run -m pytest
coverage html
```

#### Структура тестов

- `tests/test_masks.py` - базовые тесты функций маскировки карт и счетов
- `tests/test_masks_fixtures.py` - параметризованные тесты функций маскировки с использованием фикстур
- `tests/test_processing.py` - тесты функций обработки транзакций
- `tests/test_processing_fixtures.py` - параметризованные тесты функций обработки с использованием фикстур
- `tests/test_widget.py` - тесты форматирования данных и дат
- `tests/test_widget_fixtures.py` - параметризованные тесты форматирования с использованием фикстур
- `tests/conftest.py` - общие фикстуры для тестов

#### Покрытие кода

После запуска тестов с покрытием вы можете найти подробный HTML-отчет в папке `htmlcov`. Откройте файл `htmlcov/index.html` в браузере для просмотра детальной информации о покрытии кода тестами.

Для генерации отчета о покрытии:
```bash
# Запуск тестов с покрытием
coverage run -m pytest

# Генерация HTML-отчета
coverage html

# Просмотр отчета
open htmlcov/index.html
```

Текущее покрытие тестами:
- `src/masks.py`: 98% (1 строка не покрыта - проверка handlers в _setup_logger)
- `src/utils.py`: 98% (1 строка не покрыта - проверка handlers в _setup_logger)
- `src/processing.py`: 100%
- `src/widget.py`: 100%
- `src/decorators.py`: 100%
- `src/external_api.py`: 93% (5 строк не покрыты - обработка специфичных ошибок API)
- **Общее покрытие модулей src/**: 97%
- **Общее покрытие проекта**: 98%

### Структура проекта

```
PPVijetBankCard/
├── src/
│   ├── __init__.py
│   ├── masks.py          # Базовые функции маскировки
│   ├── widget.py         # Расширенные функции
│   ├── processing.py     # Функции обработки данных
│   ├── utils.py          # Утилиты для работы с JSON-файлами
│   └── external_api.py   # Функции для работы с внешними API
├── generators/
│   ├── __init__.py       # Экспорт функций генераторов
│   └── generators.py     # Генераторы для обработки данных
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Общие фикстуры для тестов
│   ├── test_masks.py     # Базовые тесты функций маскировки
│   ├── test_masks_fixtures.py  # Параметризованные тесты маскировки
│   ├── test_processing.py # Тесты функций обработки
│   ├── test_processing_fixtures.py  # Параметризованные тесты обработки
│   ├── test_widget.py    # Тесты форматирования данных
│   ├── test_widget_fixtures.py  # Параметризованные тесты форматирования
│   ├── test_generators.py     # Тесты функций-генераторов
│   ├── test_generators_fixtures.py  # Параметризованные тесты генераторов
│   ├── test_utils.py     # Тесты функций работы с JSON
│   └── test_external_api.py  # Тесты функций конвертации валют
├── htmlcov/              # Отчет о покрытии кода тестами
│   ├── index.html        # Главный файл отчета
│   └── ...               # Другие файлы отчета
├── data/
│   └── operations.json   # Файл с данными о транзакциях
├── logs/                 # Директория с файлами логов
│   ├── masks.log         # Логи модуля masks
│   └── utils.log         # Логи модуля utils
├── main.py               # Демонстрация всех функций
├── .env.example          # Шаблон файла с переменными окружения
├── requirements.txt      # Зависимости
├── pyproject.toml        # Конфигурация проекта
└── README.md             # Документация
```

### Описание модулей

| Файл                                | Описание                                                            |
|-------------------------------------|---------------------------------------------------------------------|
| `src/masks.py`                      | Базовые функции маскировки карт и счетов (с логированием)           |
| `src/widget.py`                     | Умные функции для работы со строками и датами                       |
| `src/processing.py`                 | Функции для обработки и фильтрации транзакций                       |
| `src/decorators.py`                 | Декоратор для логирования выполнения функций                        |
| `src/utils.py`                      | Функции для загрузки транзакций из JSON-файлов (с логированием)     |
| `src/external_api.py`               | Функции для конвертации валют через внешний API                     |
| `generators/generators.py`          | Генераторы для обработки данных транзакций и генерации номеров карт |
| `tests/conftest.py`                 | Общие фикстуры для тестов                                           |
| `tests/test_masks.py`               | Базовые тесты функций маскировки                                    |
| `tests/test_masks_fixtures.py`      | Параметризованные тесты функций маскировки                          |
| `tests/test_processing.py`          | Тесты функций обработки транзакций                                  |
| `tests/test_processing_fixtures.py` | Параметризованные тесты функций обработки                           |
| `tests/test_widget.py`              | Тесты форматирования данных и дат                                   |
| `tests/test_widget_fixtures.py`     | Параметризованные тесты форматирования                              |
| `tests/test_decorators.py`          | Тесты декоратора для логирования                                    |
| `tests/test_decorators_fixtures.py` | Параметризованные тесты декоратора для логирования                  |
| `tests/test_generators.py`          | Тесты функций-генераторов                                           |
| `tests/test_generators_fixtures.py` | Параметризованные тесты функций-генераторов                         |
| `tests/test_utils.py`               | Тесты функций работы с JSON-файлами                                 |
| `tests/test_external_api.py`        | Тесты функций конвертации валют                                     |
| `main.py`                           | Демонстрационная программа                                          |
| `data/operations.json`             | Файл с данными о финансовых транзакциях                             |
| `.env.example`                      | Шаблон файла с переменными окружения                                |

## Логирование

Проект использует встроенное логирование для отслеживания работы модулей `masks` и `utils`. Логи записываются в файлы в директории `logs/`.

### Автоматическое логирование

Модули `masks` и `utils` автоматически логируют свою работу:

```python
from src.masks import get_mask_card_number
from src.utils import load_transactions_from_json

# При вызове функций автоматически создаются логи
masked_card = get_mask_card_number("1234567890123456")
# → Записывается в logs/masks.log

transactions = load_transactions_from_json("data/operations.json")
# → Записывается в logs/utils.log
```

### Формат логов

Логи записываются в следующем формате:
```
<метка_времени> - <модуль> - <уровень> - <сообщение>
```

**Примеры:**
```
2025-11-19 00:45:37 - src.masks - INFO - Номер карты успешно замаскирован, длина: 16
2025-11-19 00:45:37 - src.masks - ERROR - Некорректная длина номера карты: 5
2025-11-19 00:45:37 - src.utils - INFO - Успешно загружено транзакций: 101 из файла data/operations.json
2025-11-19 00:45:37 - src.utils - WARNING - Файл не найден: nonexistent_file.json
2025-11-19 00:45:37 - src.utils - ERROR - Ошибка при загрузке файла: JSONDecodeError - ...
```

### Уровни логирования

- **DEBUG** - детальная информация для отладки
- **INFO** - информационные сообщения о нормальной работе
- **WARNING** - предупреждения о потенциальных проблемах
- **ERROR** - ошибки, которые не прерывают выполнение программы

### Файлы логов

- `logs/masks.log` - логи модуля `masks` (маскирование карт и счетов)
- `logs/utils.log` - логи модуля `utils` (загрузка транзакций)

**Важно:** Файлы логов перезаписываются при каждом запуске приложения.

### Просмотр логов

```bash
# Просмотр логов модуля masks
cat logs/masks.log

# Просмотр последних 10 строк логов
tail -n 10 logs/utils.log

# Мониторинг логов в реальном времени
tail -f logs/masks.log
```

## Обработка транзакций

Модуль `processing.py` помогает работать с финансовыми транзакциями: фильтровать, сортировать и форматировать их.

### Загрузка транзакций из JSON

```python
from src.utils import load_transactions_from_json

# Загрузка транзакций из файла
transactions = load_transactions_from_json("data/operations.json")
print(f"Загружено транзакций: {len(transactions)}")

# Функция автоматически обрабатывает ошибки:
# - Несуществующий файл → возвращает []
# - Пустой файл → возвращает []
# - Невалидный JSON → возвращает []
# - Файл с не-списком → возвращает []
```

### Конвертация валют

```python
from src.external_api import convert_currency_to_rubles

# Конвертация транзакции в рубли
transaction = {
    "operationAmount": {
        "amount": "100.0",
        "currency": {"code": "USD"}
    }
}

# Для RUB возвращает сумму как есть
rub_transaction = {
    "operationAmount": {
        "amount": "100.50",
        "currency": {"code": "RUB"}
    }
}
amount_rub = convert_currency_to_rubles(rub_transaction)
print(amount_rub)  # 100.5

# Для USD и EUR делает запрос к API
# Требуется переменная окружения API_KEY_CURRENCY
amount_in_rubles = convert_currency_to_rubles(transaction)
print(amount_in_rubles)  # Конвертированная сумма в рублях
```

**Примечание:** Для работы конвертации валют необходимо:
1. Получить API ключ на https://apilayer.com/exchangerates_data-api
2. Создать файл `.env` в корне проекта
3. Добавить в `.env`: `API_KEY_CURRENCY=ваш_ключ`

## Генераторы для обработки данных

Модуль `generators` предоставляет эффективные инструменты для работы с большими объемами данных транзакций с помощью генераторов Python. Эти генераторы позволяют финансовым аналитикам быстро и удобно находить нужную информацию о транзакциях и проводить анализ данных.

### Фильтрация транзакций по валюте

```python
from generators import filter_by_currency

# Фильтрация транзакций по USD
usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction["description"], transaction["operationAmount"]["amount"])
```

### Получение описаний транзакций

```python
from generators import transaction_descriptions

# Получение всех описаний транзакций
descriptions = transaction_descriptions(transactions)
for description in descriptions:
    print(description)
```

### Генерация номеров банковских карт

```python
from generators import card_number_generator

# Генерация номеров карт в заданном диапазоне
card_numbers = card_number_generator(1, 5)
for card_number in card_numbers:
    print(card_number)
# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005

# Генерация номеров карт в большом диапазоне
card_numbers = card_number_generator(1000, 1005)
for card_number in card_numbers:
    print(card_number)
# Вывод:
# 0000 0000 0000 1000
# 0000 0000 0000 1001
# 0000 0000 0000 1002
# 0000 0000 0000 1003
# 0000 0000 0000 1004
# 0000 0000 0000 1005
```

### Фильтрация и сортировка

```python
from src.processing import filter_by_state, sort_by_date

# Фильтрация: оставляем только выполненные транзакции
executed_transactions = filter_by_state(transactions, "EXECUTED")

# Сортировка: располагаем транзакции по дате (от новых к старым)
sorted_transactions = sort_by_date(transactions)

# Сортировка от старых к новым
sorted_asc = sort_by_date(transactions, reverse_order=False)
```

### Комплексная обработка

```python
from src.processing import format_transactions, mask_transaction_details, get_formatted_date

# Полная обработка: фильтрация + сортировка + маскирование данных
formatted = format_transactions(transactions)

# Маскирование номеров карт и счетов в одной транзакции
masked = mask_transaction_details(transaction)

# Преобразование даты в привычный формат
date_formatted = get_formatted_date(transaction)
```

**Пример результата:**
- До: `"Visa Platinum 7000792289606361"` → После: `"Visa Platinum 7000 79** **** 6361"`
- До: `"2024-03-11T02:26:18.671407"` → После: `"11.03.2024"`

## Вклад в проект

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле LICENSE.

### Краткое описание лицензии

Лицензия MIT позволяет:

- ✅ **Свободно использовать** - в личных, коммерческих и образовательных целях
- ✅ **Модифицировать** - изменять код под свои нужды
- ✅ **Распространять** - копировать и распространять оригинальный или измененный код

Единственное требование:

- 📄 **Сохранять уведомление об авторских правах** - во всех копиях или значительных частях программного обеспечения

### Использование в коммерческих продуктах

Вы можете свободно использовать этот код в коммерческих проектах без каких-либо ограничений или отчислений.

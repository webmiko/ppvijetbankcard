# Маскировка номеров карт и счетов

Проект предоставляет функции для маскировки номеров банковских карт и счетов согласно заданным правилам.

## Функциональность

Проект включает в себя две основные функции:

- `get_mask_card_number` - маскирует номер карты по правилу XXXX XX** **** XXXX
- `get_mask_account` - маскирует номер счета по правилу **XXXX

## Установка и использование

### Требования

- Python 3.8 или выше

### Установка

1. Клонируйте репозиторий:
   ``pass``

2. Перейдите в директорию проекта:
   ```bash
   cd название-проекта
   ```

3. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/macOS
   venv\Scripts\activate  # для Windows
   ```

4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

### Использование

```python
from src.utils import get_mask_card_number, get_mask_account

# Маскировка номера карты
card_number = 1234567890123456
masked_card = get_mask_card_number(card_number)
print(masked_card)  # Выведет: 1234 56** **** 3456

# Маскировка номера счета
account_number = 123456789
masked_account = get_mask_account(account_number)
print(masked_account)  # Выведет: **6789
```

## Разработка

### Инструменты

Проект использует следующие инструменты для обеспечения качества кода:

- **Black** - форматирование кода
- **isort** - сортировка импортов
- **flake8** - проверка стиля кода
- **mypy** - статическая проверка типов

### Запуск линтеров

Для проверки кода выполните следующие команды:

```bash
black .
isort .
flake8 .
mypy .
```

### Структура проекта

```
ppvijetbankcard/
│
├── src/
│   ├── __init__.py
│   └── masks.py
│
├── tests/
│   ├── __init__.py
│   └── test_masks.py
│
├── main.py
├── requirements.txt
├── .flake8
├── .gitignore
├── pyproject.toml
└── README.md
```

## Лицензия

## Вклад в проект

Вклады приветствуются! Пожалуйста, не стесняйтесь создавать pull request или открывать issue для улучшения проекта.

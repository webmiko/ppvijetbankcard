# Poetry. Оформление кода

**Приоритет: 3 (По необходимости)**  
**Источник:** `pre-code/dtbase/Poetry. Оформление кода. Шпаргалка.pdf`

## Когда использовать

Poetry используется для управления зависимостями проекта, а инструменты оформления кода (Black, Flake8, isort, mypy) - для обеспечения качества и единообразия кода.

## Poetry - управление зависимостями

### Установка Poetry
```bash
# Установка через официальный скрипт
curl -sSL https://install.python-poetry.org | python3 -

# Или через pip
pip install poetry
```

### Инициализация проекта
```bash
# Создать новый проект
poetry new my-project

# Инициализировать в существующей директории
poetry init
```

### Работа с зависимостями
```bash
# Добавить зависимость
poetry add requests
poetry add pytest --dev  # Для разработки

# Удалить зависимость
poetry remove requests

# Установить все зависимости
poetry install

# Обновить зависимости
poetry update

# Показать зависимости
poetry show
```

### pyproject.toml
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^22.0.0"
```

### Виртуальное окружение
```bash
# Активировать окружение
poetry shell

# Запустить команду в окружении
poetry run python script.py
poetry run pytest
```

## Black - форматирование кода

### Установка
```bash
pip install black
# или
poetry add black --dev
```

### Использование
```bash
# Форматировать файл
black file.py

# Форматировать директорию
black src/

# Форматировать весь проект
black .

# Проверить без изменений
black --check .

# Форматировать с указанием длины строки
black --line-length 100 .
```

### Конфигурация в pyproject.toml
```toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
```

## Flake8 - проверка стиля

### Установка
```bash
pip install flake8
# или
poetry add flake8 --dev
```

### Использование
```bash
# Проверить файл
flake8 file.py

# Проверить директорию
flake8 src/

# С игнорированием определенных ошибок
flake8 --ignore=E501,W503 src/
```

### Конфигурация в setup.cfg или .flake8
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    .venv,
    venv
```

## isort - сортировка импортов

### Установка
```bash
pip install isort
# или
poetry add isort --dev
```

### Использование
```bash
# Сортировать импорты в файле
isort file.py

# Сортировать импорты в директории
isort src/

# Проверить без изменений
isort --check-only .

# С профилем black (совместимость с Black)
isort --profile black .
```

### Конфигурация в pyproject.toml
```toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
```

## mypy - проверка типов

### Установка
```bash
pip install mypy
# или
poetry add mypy --dev
```

### Использование
```bash
# Проверить файл
mypy file.py

# Проверить директорию
mypy src/

# С строгой проверкой
mypy --strict src/
```

### Аннотации типов
```python
from typing import List, Dict, Optional

def process_data(items: List[str]) -> Dict[str, int]:
    """Обработка данных с аннотациями типов"""
    result: Dict[str, int] = {}
    for item in items:
        result[item] = len(item)
    return result

def get_user(id: int) -> Optional[Dict[str, str]]:
    """Получить пользователя или None"""
    # ...
    return None
```

### Конфигурация в pyproject.toml
```toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## Комплексная настройка

### pyproject.toml с инструментами
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^22.0.0"
flake8 = "^5.0.0"
isort = "^5.10.0"
mypy = "^0.991"

[tool.black]
line-length = 88

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.9"
```

### Pre-commit hooks
```bash
# Установка pre-commit
pip install pre-commit

# Файл: .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8

# Установка хуков
pre-commit install
```

## Приоритеты использования

### В первую очередь (по необходимости)
- **Poetry**: управление зависимостями проекта
- **Black**: автоматическое форматирование кода
- Базовые настройки инструментов

### По необходимости
- **Flake8**: проверка стиля и ошибок
- **isort**: сортировка импортов
- **mypy**: статическая проверка типов
- Pre-commit hooks для автоматизации

## Примеры из проекта

В проекте используются:
- **Poetry**: управление зависимостями через `pyproject.toml`
- **Black**: форматирование кода
- **Flake8**: проверка стиля
- **isort**: сортировка импортов
- **mypy**: проверка типов

Все инструменты настроены в `pyproject.toml` и могут быть запущены через команды:
```bash
black .
flake8 .
isort .
mypy .
```


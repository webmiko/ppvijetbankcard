# Тестирование с pytest

**Приоритет: 3 (По необходимости)**  
**Источник:** `pre-code/dtbase/Тестирование с pytest. Шпаргалка.pdf`

## Когда использовать

Тестирование используется для обеспечения качества кода, проверки корректности работы функций и предотвращения регрессий при изменениях.

## Установка pytest

```bash
pip install pytest
```

## Базовое тестирование

### Простой тест
```python
# Файл: test_example.py
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
```

### Запуск тестов
```bash
# Запуск всех тестов
pytest

# Запуск конкретного файла
pytest test_example.py

# Запуск с подробным выводом
pytest -v

# Запуск с выводом print()
pytest -s
```

## Структура тестов

### Организация тестов
```
project/
    src/
        module.py
    tests/
        __init__.py
        test_module.py
        conftest.py
```

### Именование
- Файлы тестов: `test_*.py` или `*_test.py`
- Функции тестов: `test_*`
- Классы тестов: `Test*`

## Assertions (Утверждения)

```python
def test_assertions():
    # Равенство
    assert 2 + 2 == 4
    
    # Неравенство
    assert 2 + 2 != 5
    
    # Принадлежность
    assert 'hello' in 'hello world'
    assert 'x' not in 'hello'
    
    # Типы
    assert isinstance([], list)
    
    # Истинность/ложность
    assert True
    assert not False
    
    # Сравнение
    assert 5 > 3
    assert 3 < 5
    assert 5 >= 5
```

## Фикстуры (Fixtures)

### Базовые фикстуры
```python
import pytest

@pytest.fixture
def sample_data():
    """Фикстура для подготовки данных"""
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15
```

### Фикстуры с настройкой и очисткой
```python
import pytest

@pytest.fixture
def temp_file(tmp_path):
    """Создание временного файла"""
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")
    yield file_path
    # Очистка после теста (опционально)
    file_path.unlink()
```

### Общие фикстуры (conftest.py)
```python
# Файл: tests/conftest.py
import pytest

@pytest.fixture
def sample_transaction():
    """Общая фикстура для всех тестов"""
    return {
        "id": 1,
        "amount": 100,
        "currency": "RUB"
    }
```

## Параметризация тестов

### @pytest.mark.parametrize
```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (10, -5, 5)
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

## Тестирование исключений

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Деление на ноль")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
    
    with pytest.raises(ValueError, match="Деление на ноль"):
        divide(10, 0)
```

## Мокирование (Mocking)

```python
from unittest.mock import patch, MagicMock
import pytest

def fetch_data(url):
    # Имитация запроса к API
    response = requests.get(url)
    return response.json()

@patch('requests.get')
def test_fetch_data(mock_get):
    # Настройка мока
    mock_response = MagicMock()
    mock_response.json.return_value = {'data': 'test'}
    mock_get.return_value = mock_response
    
    # Тест
    result = fetch_data('http://api.example.com')
    assert result == {'data': 'test'}
    mock_get.assert_called_once_with('http://api.example.com')
```

## Покрытие кода (Coverage)

### Установка
```bash
pip install pytest-cov
```

### Запуск с покрытием
```bash
# Запуск с покрытием
pytest --cov=src

# С HTML отчетом
pytest --cov=src --cov-report=html

# Минимальное покрытие
pytest --cov=src --cov-fail-under=80
```

## Маркеры тестов

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    # Долгий тест
    pass

@pytest.mark.skip(reason="Еще не реализовано")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Не работает на Windows")
def test_unix_only():
    pass
```

### Запуск по маркерам
```bash
# Только быстрые тесты
pytest -m "not slow"

# Только медленные
pytest -m slow
```

## Приоритеты использования

### В первую очередь (по необходимости)
- Базовые тесты с `assert`
- Запуск тестов через `pytest`
- Фикстуры для подготовки данных

### По необходимости
- Параметризация тестов
- Тестирование исключений
- Мокирование внешних зависимостей
- Измерение покрытия кода

## Примеры из проекта

В проекте тестирование используется для:
- Проверки функций маскировки (`test_masks.py`, `test_masks_fixtures.py`)
- Тестирования обработки транзакций (`test_processing.py`)
- Проверки форматирования данных (`test_widget.py`)
- Тестирования генераторов (`test_generators.py`)
- Проверки декораторов (`test_decorators.py`)


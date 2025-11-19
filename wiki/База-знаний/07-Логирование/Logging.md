# Библиотека logging

**Приоритет: 2 (Важно)**  
**Источник:** `pre-code/dtbase/Библиотека logging. Шпаргалка.pdf`

## Когда использовать

Логирование используется **всегда** для отладки, мониторинга работы приложения и отслеживания ошибок в продакшене.

## Базовое использование

### Простое логирование
```python
import logging

# Базовое логирование
logging.basicConfig(level=logging.INFO)
logging.info("Приложение запущено")
logging.warning("Предупреждение")
logging.error("Ошибка")
logging.debug("Отладочная информация")  # Не выведется (уровень INFO)
```

### Уровни логирования
```python
import logging

# По возрастанию важности:
logging.debug("Отладочная информация")      # Уровень 10
logging.info("Информационное сообщение")    # Уровень 20
logging.warning("Предупреждение")           # Уровень 30
logging.error("Ошибка")                     # Уровень 40
logging.critical("Критическая ошибка")      # Уровень 50
```

## Настройка логирования

### Базовая настройка
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("Сообщение с форматированием")
# 2024-03-15 14:30:00 - root - INFO - Сообщение с форматированием
```

### Логирование в файл
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='w',  # 'w' - перезапись, 'a' - добавление
    encoding='utf-8'
)

logging.info("Запись в файл")
```

### Логирование в файл и консоль
```python
import logging

# Создание логгера
logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)

# Обработчик для файла
file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Обработчик для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# Форматтер
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавление обработчиков
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Только в файл")
logger.warning("В файл и консоль")
```

## Логгеры для модулей

### Создание именованного логгера
```python
import logging

# Создание логгера для модуля
logger = logging.getLogger(__name__)  # Имя модуля автоматически

def process_data(data):
    logger.info(f"Обработка данных: {len(data)} элементов")
    try:
        # Код обработки
        result = data * 2
        logger.info("Данные успешно обработаны")
        return result
    except Exception as e:
        logger.error(f"Ошибка при обработке: {e}", exc_info=True)
        raise
```

### Настройка логгера модуля
```python
import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Настройка логгера для модуля"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Обработчик файла
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setLevel(level)
    
    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

# Использование
logger = setup_logger('masks', 'logs/masks.log')
logger.info("Модуль masks загружен")
```

## Форматирование сообщений

### Базовое форматирование
```python
import logging

logging.basicConfig(level=logging.INFO)

name = "Иван"
age = 25

# Старый способ
logging.info("Пользователь %s, возраст %d", name, age)

# Новый способ (f-строки)
logging.info(f"Пользователь {name}, возраст {age}")
```

### Расширенное форматирование
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
)

def process():
    logging.info("Обработка данных")
    # Выведет: 2024-03-15 14:30:00 - root - INFO - process:123 - Обработка данных
```

## Обработка исключений

```python
import logging

logging.basicConfig(level=logging.ERROR)

try:
    result = 10 / 0
except ZeroDivisionError as e:
    logging.error("Ошибка деления на ноль", exc_info=True)
    # exc_info=True выводит полный traceback
```

## Ротация логов

```python
import logging
from logging.handlers import RotatingFileHandler

# Ротация по размеру файла
handler = RotatingFileHandler(
    'app.log',
    maxBytes=10*1024*1024,  # 10 МБ
    backupCount=5,          # Хранить 5 резервных копий
    encoding='utf-8'
)

logger = logging.getLogger('my_app')
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

## Приоритеты использования

### В первую очередь (важно знать)
- Базовое логирование с `logging.basicConfig()`
- Уровни логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Логирование в файл

### По необходимости
- Именованные логгеры для модулей
- Несколько обработчиков (файл + консоль)
- Ротация логов
- Расширенное форматирование

## Примеры из проекта

В проекте логирование используется для:
- Модуля `masks.py` - логирование операций маскировки (`logs/masks.log`)
- Модуля `utils.py` - логирование загрузки транзакций (`logs/utils.log`)
- Декоратора `@log` - логирование выполнения функций (`logfile.txt`)
- Настройки через `logger_config.py`


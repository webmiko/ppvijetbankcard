# JSON, requests и datetime

**Приоритет: 2-3 (Важно - по необходимости)**  
**Источник:** `pre-code/dtbase/Библиотеки json, requests и datetime. Шпаргалка.pdf`

## Когда использовать

- **JSON** - при работе с API, конфигурационными файлами, данными веб-приложений
- **requests** - для HTTP-запросов к внешним API
- **datetime** - для работы с датами и временем

## JSON

### Чтение JSON
```python
import json

# Из строки
json_string = '{"name": "Иван", "age": 25}'
data = json.loads(json_string)  # {'name': 'Иван', 'age': 25}

# Из файла
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### Запись JSON
```python
import json

data = {'name': 'Иван', 'age': 25}

# В строку
json_string = json.dumps(data)  # '{"name": "Иван", "age": 25}'
json_string_pretty = json.dumps(data, ensure_ascii=False, indent=2)

# В файл
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### Обработка ошибок
```python
import json

try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Файл не найден")
    data = []
except json.JSONDecodeError:
    print("Ошибка парсинга JSON")
    data = []
```

## requests

### Установка
```bash
pip install requests
```

### GET запрос
```python
import requests

# Простой запрос
response = requests.get('https://api.example.com/data')

# С параметрами
params = {'key': 'value', 'page': 1}
response = requests.get('https://api.example.com/data', params=params)

# Проверка статуса
if response.status_code == 200:
    data = response.json()  # Автоматический парсинг JSON
    print(data)
```

### POST запрос
```python
import requests

# С данными
data = {'name': 'Иван', 'age': 25}
response = requests.post('https://api.example.com/users', json=data)

# С заголовками
headers = {'Authorization': 'Bearer token'}
response = requests.post('https://api.example.com/data', json=data, headers=headers)
```

### Обработка ошибок
```python
import requests

try:
    response = requests.get('https://api.example.com/data', timeout=5)
    response.raise_for_status()  # Вызовет исключение при ошибке HTTP
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e}")
except requests.exceptions.Timeout:
    print("Превышено время ожидания")
except requests.exceptions.HTTPError as e:
    print(f"HTTP ошибка: {e}")
```

## datetime

### Создание объектов даты и времени
```python
from datetime import datetime, date, time, timedelta

# Текущая дата и время
now = datetime.now()
today = date.today()

# Конкретная дата
dt = datetime(2024, 3, 15, 14, 30, 0)  # 2024-03-15 14:30:00
d = date(2024, 3, 15)  # 2024-03-15

# Из строки
dt = datetime.strptime('2024-03-15 14:30:00', '%Y-%m-%d %H:%M:%S')
```

### Форматирование дат
```python
from datetime import datetime

now = datetime.now()

# В строку
formatted = now.strftime('%d.%m.%Y %H:%M:%S')  # '15.03.2024 14:30:00'
date_only = now.strftime('%d.%m.%Y')  # '15.03.2024'

# ISO формат
iso_string = now.isoformat()  # '2024-03-15T14:30:00'
```

### Работа с временными интервалами
```python
from datetime import datetime, timedelta

now = datetime.now()

# Добавление времени
tomorrow = now + timedelta(days=1)
next_week = now + timedelta(weeks=1)
in_hour = now + timedelta(hours=1)

# Разница между датами
diff = tomorrow - now
print(diff.days)  # 1
print(diff.total_seconds())  # 86400.0
```

### Часовые пояса
```python
from datetime import datetime, timezone, timedelta

# UTC
utc_now = datetime.now(timezone.utc)

# Локальное время
local_now = datetime.now()

# Конкретный часовой пояс
tz = timezone(timedelta(hours=3))
moscow_time = datetime.now(tz)
```

## Приоритеты использования

### В первую очередь (важно знать)
- **JSON**: `json.load()`, `json.dump()` для работы с файлами
- **datetime**: `datetime.now()`, `strftime()`, `strptime()` для форматирования
- Базовые операции с датами

### По необходимости
- **requests**: для работы с внешними API
- Продвинутые операции с датами (timedelta, timezone)
- Обработка ошибок при работе с JSON и requests

## Примеры из проекта

В проекте используются:
- **JSON**: загрузка транзакций из `data/operations.json` (`load_transactions_from_json`)
- **datetime**: форматирование дат транзакций (`get_date`, `get_formatted_date`)
- **requests**: конвертация валют через внешний API (`convert_currency_to_rubles`)


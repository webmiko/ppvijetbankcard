# CSV и pandas

**Приоритет: 3 (По необходимости)**  
**Источник:** `pre-code/dtbase/Библиотеки csv и pandas. Шпаргалка.pdf`

## Когда использовать

- **CSV** - для простой работы с табличными данными в текстовом формате
- **pandas** - для анализа больших объемов табличных данных, сложных операций с данными

## CSV (встроенный модуль)

### Чтение CSV
```python
import csv

# Чтение из файла
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# Чтение как словарь
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['age'])
```

### Запись CSV
```python
import csv

data = [
    ['Иван', 25, 'Москва'],
    ['Петр', 30, 'СПб']
]

# Запись списков
with open('output.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Имя', 'Возраст', 'Город'])  # Заголовки
    writer.writerows(data)

# Запись словарей
data_dict = [
    {'name': 'Иван', 'age': 25, 'city': 'Москва'},
    {'name': 'Петр', 'age': 30, 'city': 'СПб'}
]

with open('output.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age', 'city'])
    writer.writeheader()
    writer.writerows(data_dict)
```

## pandas

### Установка
```bash
pip install pandas
```

### Основные структуры данных

#### DataFrame (таблица)
```python
import pandas as pd

# Создание из словаря
data = {
    'name': ['Иван', 'Петр', 'Мария'],
    'age': [25, 30, 28],
    'city': ['Москва', 'СПб', 'Казань']
}
df = pd.DataFrame(data)

# Чтение из CSV
df = pd.read_csv('data.csv', encoding='utf-8')

# Чтение из JSON
df = pd.read_json('data.json')
```

#### Series (столбец)
```python
import pandas as pd

# Создание Series
ages = pd.Series([25, 30, 28], name='age')

# Доступ к элементам
first_age = ages[0]  # 25
```

### Базовые операции

#### Просмотр данных
```python
import pandas as pd

df = pd.read_csv('data.csv')

# Первые строки
df.head()        # Первые 5 строк
df.head(10)      # Первые 10 строк

# Последние строки
df.tail()        # Последние 5 строк

# Информация о данных
df.info()        # Типы данных, количество строк
df.describe()    # Статистика по числовым столбцам
df.shape         # (количество_строк, количество_столбцов)
```

#### Доступ к данным
```python
import pandas as pd

df = pd.read_csv('data.csv')

# По столбцу
names = df['name']
names = df.name  # Альтернативный способ

# По строке
first_row = df.iloc[0]        # По индексу
row_by_label = df.loc[0]      # По метке

# Фильтрация
young = df[df['age'] < 30]    # Возраст меньше 30
moscow = df[df['city'] == 'Москва']
```

#### Изменение данных
```python
import pandas as pd

df = pd.read_csv('data.csv')

# Добавление столбца
df['new_column'] = df['age'] * 2

# Удаление столбца
df = df.drop('column_name', axis=1)

# Удаление строк
df = df.drop([0, 1])  # Удалить строки с индексами 0 и 1
```

#### Группировка и агрегация
```python
import pandas as pd

df = pd.read_csv('data.csv')

# Группировка
grouped = df.groupby('city')

# Агрегация
avg_age_by_city = grouped['age'].mean()        # Средний возраст по городам
count_by_city = grouped.size()                  # Количество по городам
sum_by_city = grouped['age'].sum()             # Сумма по городам
```

#### Сортировка
```python
import pandas as pd

df = pd.read_csv('data.csv')

# Сортировка по столбцу
df_sorted = df.sort_values('age')               # По возрастанию
df_sorted = df.sort_values('age', ascending=False)  # По убыванию

# Сортировка по нескольким столбцам
df_sorted = df.sort_values(['city', 'age'])
```

#### Обработка пропусков
```python
import pandas as pd

df = pd.read_csv('data.csv')

# Проверка пропусков
df.isnull()          # Булева таблица пропусков
df.isnull().sum()    # Количество пропусков по столбцам

# Удаление строк с пропусками
df_clean = df.dropna()

# Заполнение пропусков
df_filled = df.fillna(0)                    # Заполнить нулями
df_filled = df.fillna(df['age'].mean())     # Заполнить средним
```

### Запись данных
```python
import pandas as pd

df = pd.read_csv('data.csv')

# В CSV
df.to_csv('output.csv', index=False, encoding='utf-8')

# В JSON
df.to_json('output.json', orient='records', force_ascii=False)

# В Excel (требует openpyxl)
df.to_excel('output.xlsx', index=False)
```

## Приоритеты использования

### В первую очередь (по необходимости)
- **CSV**: базовое чтение и запись для простых задач
- **pandas**: чтение данных (`read_csv`, `read_json`)

### По необходимости
- **pandas**: фильтрация, группировка, агрегация для анализа данных
- Обработка пропусков
- Сложные операции с данными

## Примеры использования

### CSV - для простых задач
```python
import csv

# Простое чтение табличных данных
with open('transactions.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    transactions = list(reader)
```

### pandas - для анализа
```python
import pandas as pd

# Анализ транзакций
df = pd.read_json('operations.json')
total_by_currency = df.groupby('currency')['amount'].sum()
avg_amount = df['amount'].mean()
```

## Примеры из проекта

В проекте CSV и pandas могут использоваться для:
- Экспорта транзакций в CSV формат
- Анализа больших объемов транзакционных данных
- Генерации отчетов и статистики


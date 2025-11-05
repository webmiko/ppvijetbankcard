import os
import tempfile
from typing import Any, Callable, Dict, Generator, List, Tuple, Union

import pytest

from src.decorators import log


@pytest.fixture
def temp_log_file() -> Generator[str, None, None]:
    """Фикстура, создающая временный файл для логов.

    Yields:
        str: Имя временного файла
    """
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        filename: str = temp_file.name

    # Возвращаем имя файла для использования в тестах
    yield filename

    # Удаляем временный файл после использования
    if os.path.exists(filename):
        os.unlink(filename)


@pytest.fixture
def sample_functions() -> Dict[str, Callable[..., Union[int, float, str]]]:
    """Фикстура с примерами функций для тестирования декоратора.

    Returns:
        Dict[str, Callable]: Словарь с функциями для тестирования
    """

    # Определяем тестовые функции
    def add(a: int, b: int) -> int:
        """Функция сложения двух чисел."""
        return a + b

    def multiply(a: int, b: int) -> int:
        """Функция умножения двух чисел."""
        return a * b

    def divide(a: int, b: int) -> float:
        """Функция деления двух чисел."""
        return a / b

    def subtract(a: int, b: int) -> int:
        """Функция вычитания двух чисел."""
        if a < b:
            raise ValueError("Результат не может быть отрицательным")
        return a - b

    def greet(name: str = "Гость") -> str:
        """Функция приветствия."""
        return f"Привет, {name}!"

    # Возвращаем словарь с функциями
    return {"add": add, "multiply": multiply, "divide": divide, "subtract": subtract, "greet": greet}


@pytest.fixture
def error_cases() -> List[Tuple[Callable[..., Union[int, float]], Tuple, Dict, str]]:
    """Фикстура с примерами функций и аргументов, вызывающих ошибки.

    Returns:
        List[Tuple]: Список кортежей (функция, аргументы, kwargs, тип ошибки)
    """

    # Определяем функции, вызывающие ошибки
    def divide_by_zero(a: int, b: int) -> float:
        """Функция деления, которая вызовет ошибку при делении на ноль."""
        return a / b

    def invalid_operation(a: int, b: int) -> int:
        """Функция с проверкой аргументов, которая вызовет ошибку при отрицательных значениях."""
        if a < 0 or b < 0:
            raise ValueError("Аргументы должны быть положительными")
        return a + b

    def type_error(a: Any, b: int) -> int:
        """Функция, которая вызовет ошибку TypeError при некорректном типе первого аргумента."""
        return int(a) + b  # Это вызовет TypeError, если a не является числом

    # Возвращаем список тестовых случаев
    return [
        (divide_by_zero, (10, 0), {}, "ZeroDivisionError"),
        (invalid_operation, (-5, 3), {}, "ValueError"),
        (type_error, ("строка", 5), {}, "TypeError"),
    ]


@pytest.mark.parametrize(
    "function_name,args,kwargs,expected_result",
    [
        ("add", (1, 2), {}, 3),
        ("multiply", (3, 4), {}, 12),
        ("divide", (10, 2), {}, 5.0),
        ("subtract", (10, 5), {}, 5),
        ("greet", (), {"name": "Мир"}, "Привет, Мир!"),
    ],
)
def test_log_success_to_file(
    function_name: str,
    args: Tuple,
    kwargs: Dict,
    expected_result: Any,
    sample_functions: Dict[str, Callable],
    temp_log_file: str,
) -> None:
    """Тестирование успешного выполнения функций с логированием в файл.

    Args:
        function_name: Имя функции для тестирования
        args: Позиционные аргументы функции
        kwargs: Именованные аргументы функции
        expected_result: Ожидаемый результат выполнения функции
        sample_functions: Фикстура с функциями для тестирования
        temp_log_file: Фикстура с временным файлом для логов
    """
    # Получаем функцию из фикстуры
    func = sample_functions[function_name]

    # Применяем декоратор с указанием файла для логов
    decorated_func = log(filename=temp_log_file)(func)

    # Вызываем функцию с тестовыми данными
    result = decorated_func(*args, **kwargs)

    # Проверяем результат
    assert result == expected_result, f"Ожидали {expected_result}, получили {result}"

    # Проверяем содержимое файла логов
    with open(temp_log_file, encoding="utf-8") as file:
        log_content = file.read()

    # Проверяем наличие записи в логе
    assert (
        f"{function_name} ok" in log_content
    ), f"В файле лога отсутствует запись о выполнении функции {function_name}: {log_content}"


@pytest.mark.parametrize(
    "func,args,kwargs,error_type",
    [
        (lambda a, b: a / b, (10, 0), {}, "ZeroDivisionError"),
        (lambda a, b: int(a) + int(b), ("abc", 3), {}, "ValueError"),
    ],
)
def test_log_error_to_file(
    func: Callable[..., Any], args: Tuple, kwargs: Dict, error_type: str, temp_log_file: str
) -> None:
    """Тестирование обработки ошибок с логированием в файл.

    Args:
        func: Тестируемая функция
        args: Позиционные аргументы функции
        kwargs: Именованные аргументы функции
        error_type: Ожидаемый тип ошибки
        temp_log_file: Фикстура с временным файлом для логов
    """
    # Применяем декоратор с указанием файла для логов
    decorated_func = log(filename=temp_log_file)(func)

    # Вызываем функцию и ожидаем ошибку
    try:
        decorated_func(*args, **kwargs)
        assert False, f"Ожидалось исключение {error_type}"
    except (ZeroDivisionError, ValueError) as e:
        # Ожидаемая ошибка - проверяем тип
        assert type(e).__name__ == error_type, f"Ожидали {error_type}, получили {type(e).__name__}"
        # Выводим информацию о ней
        print(f"Перехвачено ожидаемое исключение: {type(e).__name__}: {e}")

    # Проверяем содержимое файла логов
    with open(temp_log_file, encoding="utf-8") as file:
        log_content = file.read()

    # Проверяем наличие записи об ошибке в логе
    assert (
        f"error: {error_type}" in log_content
    ), f"В файле лога отсутствует запись об ошибке {error_type}: {log_content}"
    assert (
        f"Inputs: {args}, {kwargs}" in log_content
    ), f"В файле лога отсутствует информация о входных данных: {log_content}"


def test_log_multiple_calls_to_file(sample_functions: Dict[str, Callable], temp_log_file: str) -> None:
    """Тестирование логирования при многократных вызовах функций.

    Args:
        sample_functions: Фикстура с функциями для тестирования
        temp_log_file: Фикстура с временным файлом для логов
    """
    # Применяем декоратор к функциям
    add = log(filename=temp_log_file)(sample_functions["add"])
    multiply = log(filename=temp_log_file)(sample_functions["multiply"])

    # Определяем тестовые данные
    test_cases: List[Tuple[Callable[..., Any], Tuple, Dict]] = [
        (add, (1, 2), {}),
        (multiply, (3, 4), {}),
        (add, (5, 6), {}),
    ]

    # Вызываем функции несколько раз
    for func, args, kwargs in test_cases:
        func(*args, **kwargs)

    # Проверяем содержимое файла логов
    with open(temp_log_file, encoding="utf-8") as file:
        log_content = file.read()

    # Проверяем, что все вызовы были залогированы
    add_calls = log_content.count("add ok")
    multiply_calls = log_content.count("multiply ok")

    assert add_calls == 2, f"Ожидали 2 вызова функции add, получили {add_calls}: {log_content}"
    assert multiply_calls == 1, f"Ожидали 1 вызов функции multiply, получили {multiply_calls}: {log_content}"


@pytest.mark.parametrize("filename", [None, ""])
def test_log_to_console(filename: str, sample_functions: Dict[str, Callable], capsys: Any) -> None:
    """Тестирование логирования в консоль.

    Args:
        filename: Имя файла для логов (None или пустая строка для вывода в консоль)
        sample_functions: Фикстура с функциями для тестирования
        capsys: Фикстура для перехвата вывода в консоль
    """
    # Применяем декоратор с выводом в консоль
    add = log(filename=filename)(sample_functions["add"])

    # Определяем тестовые данные
    test_a: int = 1
    test_b: int = 2
    expected_result: int = 3

    # Вызываем функцию
    result = add(test_a, test_b)

    # Проверяем результат
    assert result == expected_result, f"Ожидали {expected_result}, получили {result}"

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "add ok" in captured.out, f"В консоли отсутствует запись о выполнении функции: {captured.out}"


def test_log_with_none_filename(sample_functions: Dict[str, Callable], capsys: Any) -> None:
    """Тестирование логирования в консоль при передаче None.

    Args:
        sample_functions: Фикстура с функциями для тестирования
        capsys: Фикстура для перехвата вывода в консоль
    """
    # Применяем декоратор с выводом в консоль
    add = log(filename=None)(sample_functions["add"])

    # Определяем тестовые данные
    test_a: int = 1
    test_b: int = 2
    expected_result: int = 3

    # Вызываем функцию
    result = add(test_a, test_b)

    # Проверяем результат
    assert result == expected_result, f"Ожидали {expected_result}, получили {result}"

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "add ok" in captured.out, f"В консоли отсутствует запись о выполнении функции: {captured.out}"


def test_log_with_default_filename(sample_functions: Dict[str, Callable], monkeypatch: Any) -> None:
    """Тестирование логирования в файл по умолчанию (logfile.txt).

    Args:
        sample_functions: Фикстура с функциями для тестирования
        monkeypatch: Фикстура для модификации поведения функций
    """
    # Создаем временный файл вместо logfile.txt
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as temp_file:
        temp_filename = temp_file.name

    try:
        # Заменяем функцию open для перенаправления записи в наш временный файл
        original_open = open

        def mock_open(filename: str, *args: Any, **kwargs: Any) -> Any:
            """Функция-заглушка для перенаправления записи в logfile.txt в наш временный файл."""
            if filename == "logfile.txt":
                return original_open(temp_filename, *args, **kwargs)
            return original_open(filename, *args, **kwargs)

        # Применяем monkeypatch
        monkeypatch.setattr("builtins.open", mock_open)

        # Импортируем декоратор после monkeypatch
        from src.decorators import log as patched_log

        # Применяем декоратор с именем файла по умолчанию
        add = patched_log()(sample_functions["add"])

        # Определяем тестовые данные
        test_a: int = 1
        test_b: int = 2
        expected_result: int = 3

        # Вызываем функцию
        result = add(test_a, test_b)

        # Проверяем результат
        assert result == expected_result, f"Ожидали {expected_result}, получили {result}"

        # Проверяем содержимое файла логов
        with open(temp_filename, encoding="utf-8") as file:
            log_content = file.read()

        # Проверяем наличие записи в логе
        assert "add ok" in log_content, f"В файле лога отсутствует запись о выполнении функции: {log_content}"
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)

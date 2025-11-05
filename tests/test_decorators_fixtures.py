import os
import tempfile
from typing import Any, Callable, Dict, Generator, List, Tuple

import pytest

from src.decorators import log


@pytest.fixture
def temp_log_file() -> Generator[str, None, None]:
    """Фикстура, создающая временный файл для логов."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        filename: str = temp_file.name
    yield filename
    # Удаляем временный файл после использования
    if os.path.exists(filename):
        os.unlink(filename)


@pytest.fixture
def sample_functions() -> Dict[str, Callable]:
    """Фикстура с примерами функций для тестирования декоратора."""

    def add(a: int, b: int) -> int:
        return a + b

    def multiply(a: int, b: int) -> int:
        return a * b

    def divide(a: int, b: int) -> float:
        return a / b

    def subtract(a: int, b: int) -> int:
        if a < b:
            raise ValueError("Результат не может быть отрицательным")
        return a - b

    def greet(name: str = "Гость") -> str:
        return f"Привет, {name}!"

    return {"add": add, "multiply": multiply, "divide": divide, "subtract": subtract, "greet": greet}


@pytest.fixture
def error_cases() -> List[Tuple[Callable, Tuple, Dict, str]]:
    """Фикстура с примерами функций и аргументов, вызывающих ошибки."""

    def divide_by_zero(a: int, b: int) -> float:
        return a / b

    def invalid_operation(a: int, b: int) -> int:
        if a < 0 or b < 0:
            raise ValueError("Аргументы должны быть положительными")
        return a + b

    def type_error(a: Any, b: int) -> int:
        return int(a) + b  # Это вызовет TypeError, если a не является числом

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
    """Тестирование успешного выполнения функций с логированием в файл."""
    # Получаем функцию из фикстуры
    func = sample_functions[function_name]

    # Применяем декоратор с указанием файла для логов
    decorated_func = log(filename=temp_log_file)(func)

    # Вызываем функцию
    result = decorated_func(*args, **kwargs)

    # Проверяем результат
    assert result == expected_result

    # Проверяем содержимое файла логов
    with open(temp_log_file, encoding="utf-8") as file:
        log_content = file.read()

    assert f"{function_name} ok" in log_content


@pytest.mark.parametrize(
    "func,args,kwargs,error_type",
    [
        (lambda a, b: a / b, (10, 0), {}, "ZeroDivisionError"),
        (lambda a, b: int(a) + int(b), ("abc", 3), {}, "ValueError"),
    ],
)
def test_log_error_to_file(func: Callable, args: Tuple, kwargs: Dict, error_type: str, temp_log_file: str) -> None:
    """Тестирование обработки ошибок с логированием в файл."""
    # Применяем декоратор с указанием файла для логов
    decorated_func = log(filename=temp_log_file)(func)

    # Вызываем функцию и ожидаем ошибку
    try:
        decorated_func(*args, **kwargs)
        assert False, "Ожидалось исключение"
    except (ZeroDivisionError, ValueError) as e:
        # Ожидаемая ошибка - выводим информацию о ней
        print(f"Перехвачено ожидаемое исключение: {type(e).__name__}: {e}")

    # Проверяем содержимое файла логов
    with open(temp_log_file, encoding="utf-8") as file:
        log_content = file.read()

    assert f"error: {error_type}" in log_content
    assert f"Inputs: {args}, {kwargs}" in log_content


def test_log_multiple_calls_to_file(sample_functions: Dict[str, Callable], temp_log_file: str) -> None:
    """Тестирование логирования при многократных вызовах функций."""
    # Применяем декоратор к функциям
    add = log(filename=temp_log_file)(sample_functions["add"])
    multiply = log(filename=temp_log_file)(sample_functions["multiply"])

    # Вызываем функции несколько раз
    add(1, 2)
    multiply(3, 4)
    add(5, 6)

    # Проверяем содержимое файла логов
    with open(temp_log_file, encoding="utf-8") as file:
        log_content = file.read()

    # Проверяем, что все вызовы были залогированы
    assert log_content.count("add ok") == 2
    assert log_content.count("multiply ok") == 1


@pytest.mark.parametrize("filename", [None, ""])
def test_log_to_console(filename: str, sample_functions: Dict[str, Callable], capsys: Any) -> None:
    """Тестирование логирования в консоль."""
    # Применяем декоратор с выводом в консоль
    add = log(filename=filename)(sample_functions["add"])

    # Вызываем функцию
    result = add(1, 2)

    # Проверяем результат
    assert result == 3

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_with_none_filename(sample_functions: Dict[str, Callable], capsys: Any) -> None:
    """Тестирование логирования в консоль при передаче None."""
    # Применяем декоратор с выводом в консоль
    add = log(filename=None)(sample_functions["add"])

    # Вызываем функцию
    result = add(1, 2)

    # Проверяем результат
    assert result == 3

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_with_default_filename(sample_functions: Dict[str, Callable], monkeypatch: Any) -> None:
    """Тестирование логирования в файл по умолчанию (logfile.txt)."""
    # Создаем временный файл вместо logfile.txt
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as temp_file:
        temp_filename = temp_file.name

    try:
        # Заменяем функцию open для перенаправления записи в наш временный файл
        original_open = open

        def mock_open(filename: str, *args: Any, **kwargs: Any) -> Any:
            if filename == "logfile.txt":
                return original_open(temp_filename, *args, **kwargs)
            return original_open(filename, *args, **kwargs)

        monkeypatch.setattr("builtins.open", mock_open)

        # Импортируем декоратор после monkeypatch
        from src.decorators import log as patched_log

        # Применяем декоратор с именем файла по умолчанию
        add = patched_log()(sample_functions["add"])

        # Вызываем функцию
        result = add(1, 2)

        # Проверяем результат
        assert result == 3

        # Проверяем содержимое файла логов
        with open(temp_filename, encoding="utf-8") as file:
            log_content = file.read()

        assert "add ok" in log_content
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)

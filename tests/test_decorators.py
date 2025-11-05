import os
import tempfile
from typing import Any

from src.decorators import log


def test_log_to_file() -> None:
    """Тестирование логирования в файл при успешном выполнении функции."""
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        filename: str = temp_file.name

    # Определяем тестовую функцию с декоратором
    @log(filename=filename)
    def add(a: int, b: int) -> int:
        """Тестовая функция сложения."""
        return a + b

    # Выполняем тестовый сценарий
    test_a: int = 1
    test_b: int = 2
    expected_result: int = 3

    # Вызов функции
    result: int = add(test_a, test_b)

    # Проверка результата
    assert result == expected_result, f"Ожидали {expected_result}, получили {result}"

    # Проверка содержимого файла лога
    with open(filename, encoding="utf-8") as file:
        log_content: str = file.read()

    # Проверяем наличие записи в логе
    assert "add ok" in log_content, f"В файле лога отсутствует запись о выполнении функции: {log_content}"

    # Удаляем временный файл
    os.unlink(filename)


def test_log_to_file_with_error() -> None:
    """Тестирование логирования в файл при возникновении ошибки."""
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        filename: str = temp_file.name

    # Определяем тестовую функцию с декоратором
    @log(filename=filename)
    def divide(a: int, b: int) -> float:
        """Тестовая функция деления."""
        return a / b

    # Определяем тестовые данные
    test_a: int = 1
    test_b: int = 0  # Это вызовет ошибку деления на ноль

    # Вызов функции с ожидаемой ошибкой
    try:
        divide(test_a, test_b)
        assert False, "Ожидалось исключение ZeroDivisionError"
    except ZeroDivisionError as e:
        # Ожидаемая ошибка - проверяем тип и сообщение
        assert isinstance(e, ZeroDivisionError)

    # Проверка содержимого файла лога
    with open(filename, encoding="utf-8") as file:
        log_content: str = file.read()

    # Проверяем наличие записи об ошибке в логе
    assert (
        "divide error: ZeroDivisionError" in log_content
    ), f"В файле лога отсутствует запись об ошибке: {log_content}"
    assert (
        f"Inputs: ({test_a}, {test_b}), {{" + "}" in log_content
    ), f"В файле лога отсутствует информация о входных данных: {log_content}"

    # Удаляем временный файл
    os.unlink(filename)


def test_log_to_console(capsys: Any) -> None:
    """Тестирование логирования в консоль при успешном выполнении функции."""

    # Определяем тестовую функцию с декоратором
    @log(None)
    def multiply(a: int, b: int) -> int:
        """Тестовая функция умножения."""
        return a * b

    # Определяем тестовые данные
    test_a: int = 3
    test_b: int = 4
    expected_result: int = 12

    # Вызов функции
    result: int = multiply(test_a, test_b)

    # Проверка результата
    assert result == expected_result, f"Ожидали {expected_result}, получили {result}"

    # Проверка вывода в консоль
    captured = capsys.readouterr()
    assert "multiply ok" in captured.out, f"В консоли отсутствует запись о выполнении функции: {captured.out}"


def test_log_to_console_with_error(capsys: Any) -> None:
    """Тестирование логирования в консоль при возникновении ошибки."""

    # Определяем тестовую функцию с декоратором
    @log(None)
    def subtract(a: int, b: int) -> int:
        """Тестовая функция вычитания."""
        if a < b:
            raise ValueError("Результат не может быть отрицательным")
        return a - b

    # Определяем тестовые данные
    test_a: int = 2
    test_b: int = 5  # Это вызовет ошибку

    # Вызов функции с ожидаемой ошибкой
    try:
        subtract(test_a, test_b)
        assert False, "Ожидалось исключение ValueError"
    except ValueError as e:
        # Ожидаемая ошибка - проверяем тип и сообщение
        assert isinstance(e, ValueError)
        assert str(e) == "Результат не может быть отрицательным"

    # Проверка вывода в консоль
    captured = capsys.readouterr()
    assert "subtract error: ValueError" in captured.out, f"В консоли отсутствует запись об ошибке: {captured.out}"
    assert (
        f"Inputs: ({test_a}, {test_b}), {{" + "}" in captured.out
    ), f"В консоли отсутствует информация о входных данных: {captured.out}"

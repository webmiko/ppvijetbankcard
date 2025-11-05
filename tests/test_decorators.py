import os
import tempfile
from typing import Any

from src.decorators import log


def test_log_to_file() -> None:
    """Тестирование логирования в файл при успешном выполнении функции."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        filename: str = temp_file.name

    @log(filename=filename)
    def add(a: int, b: int) -> int:
        return a + b

    # Вызов функции
    result: int = add(1, 2)

    # Проверка результата
    assert result == 3

    # Проверка содержимого файла лога
    with open(filename, encoding="utf-8") as file:
        log_content: str = file.read()

    assert "add ok" in log_content

    # Удаляем временный файл
    os.unlink(filename)


def test_log_to_file_with_error() -> None:
    """Тестирование логирования в файл при возникновении ошибки."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        filename: str = temp_file.name

    @log(filename=filename)
    def divide(a: int, b: int) -> float:
        return a / b

    # Вызов функции с ошибкой
    try:
        divide(1, 0)
    except ZeroDivisionError:
        pass  # Ожидаемая ошибка

    # Проверка содержимого файла лога
    with open(filename, encoding="utf-8") as file:
        log_content: str = file.read()

    assert "divide error: ZeroDivisionError" in log_content
    assert "Inputs: (1, 0), {}" in log_content

    # Удаляем временный файл
    os.unlink(filename)


def test_log_to_console(capsys: Any) -> None:
    """Тестирование логирования в консоль при успешном выполнении функции."""

    @log(None)
    def multiply(a: int, b: int) -> int:
        return a * b

    # Вызов функции
    result: int = multiply(3, 4)

    # Проверка результата
    assert result == 12

    # Проверка вывода в консоль
    captured = capsys.readouterr()
    assert "multiply ok" in captured.out


def test_log_to_console_with_error(capsys: Any) -> None:
    """Тестирование логирования в консоль при возникновении ошибки."""

    @log(None)
    def subtract(a: int, b: int) -> int:
        if a < b:
            raise ValueError("Результат не может быть отрицательным")
        return a - b

    # Вызов функции с ошибкой
    try:
        subtract(2, 5)
    except ValueError:
        pass  # Ожидаемая ошибка

    # Проверка вывода в консоль
    captured = capsys.readouterr()
    assert "subtract error: ValueError" in captured.out
    assert "Inputs: (2, 5), {}" in captured.out

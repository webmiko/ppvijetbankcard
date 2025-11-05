import sys
from datetime import datetime
from typing import Any, Callable, Optional, TextIO


def log(filename: Optional[str] = "logfile.txt") -> Callable[..., Any]:
    """
    Декоратор для логирования начала и конца выполнения функции,
    а также ее результатов или возникших ошибок.

    Args:
        filename: Имя файла для записи логов. По умолчанию используется
                 файл "logfile.txt". Если передано значение None или пустая строка,
                 логи выводятся в консоль.

    Returns:
        Callable: Декорированная функция
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Определяем, куда выводить логи
            log_output: TextIO
            if filename:
                log_output = open(filename, "a", encoding="utf-8")
                is_file_output = True
            else:
                log_output = sys.stdout
                is_file_output = False

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)
                # Записываем успешное выполнение
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_output.write(f"[{timestamp}] {func.__name__} ok\n")
                # Сбрасываем буфер, если вывод в консоль
                if not is_file_output:
                    log_output.flush()
                return result
            except Exception as e:
                # Записываем ошибку
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_type = type(e).__name__
                error_message = f"[{timestamp}] {func.__name__} error: {error_type}. "

                if isinstance(e, ZeroDivisionError):
                    error_message += f"Деление на ноль невозможно! Inputs: {args}, {kwargs}\n"
                else:
                    error_message += f"Inputs: {args}, {kwargs}\n"

                log_output.write(error_message)
                # Сбрасываем буфер, если вывод в консоль
                if not is_file_output:
                    log_output.flush()
                raise
            finally:
                # Закрываем файл, если он был открыт
                if is_file_output:
                    log_output.close()

        return wrapper

    return decorator

import sys
from datetime import datetime
from typing import Any, Callable, Optional


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
            to_file = filename is not None and filename != ""
            log_output = open(filename, "a", encoding="utf-8") if to_file and filename is not None else sys.stdout

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)
                # Записываем успешное выполнение
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_output.write(f"[{timestamp}] {func.__name__} ok\n")
                # Сбрасываем буфер, если вывод в консоль
                if not to_file:
                    log_output.flush()
                return result
            except Exception as e:
                # Записываем ошибку
                error_type = type(e).__name__
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if error_type == "ZeroDivisionError":
                    log_output.write(
                        f"[{timestamp}] {func.__name__} error: {error_type}. "
                        f"Деление на ноль невозможно! Inputs: {args}, {kwargs}\n"
                    )
                else:
                    log_output.write(f"[{timestamp}] {func.__name__} error: {error_type}. " f"Inputs: {args}, {kwargs}\n")
                # Сбрасываем буфер, если вывод в консоль
                if not to_file:
                    log_output.flush()
                raise
            finally:
                # Закрываем файл, если он был открыт
                if to_file:
                    log_output.close()

        return wrapper

    return decorator

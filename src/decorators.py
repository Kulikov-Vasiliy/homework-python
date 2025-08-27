import os

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "mylog.txt")


def log(filename=None):
    """Декоратор автоматически логирует начало и конец выполнения функции,
    а также ее результаты или возникшие ошибки."""

    def decorator(func):
        def wrapper(*args, **kwargs: int or str) -> int or str:

            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok. Result: {result}"
                if filename:
                    with open(DATA_PATH, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                else:
                    print(message)
                return result

            except Exception as e:
                message = f"{func.__name__} error: {str(e)}. Inputs: {args}, {kwargs}"
                if filename:
                    with open(DATA_PATH, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                else:
                    print(message)
                raise

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x, y: int or str) -> int or str:  # type: ignore
    return x + y

import os

# Путь к текущему файлу
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "mylog.txt")

def log(filename=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
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
def my_function(x, y):
    return x + y

my_function(1, 2)
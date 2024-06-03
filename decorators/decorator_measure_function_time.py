from datetime import datetime
import functools
import time


def measure_function_time(func):
    """Decorator to measure the execution time of a function.

    Args:
        func: The function to be decorated.

    Returns:
        A wrapper function that executes the decorated function and prints its execution time.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        results = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.2f} seconds")
        return results

    return wrapper


def log_runtime(log_file_path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            runtime = end_time - start_time
            seperator = 100 * "="
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            with open(log_file_path, "a") as log_file:
                log_file.write(
                    f"""
                {seperator}
                (Started {timestamp}) Function {func.__name__} executed in {runtime:.4f} seconds\n
"""
                )
            return result

        return wrapper

    return decorator

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


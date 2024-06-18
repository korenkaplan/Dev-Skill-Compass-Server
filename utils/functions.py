import logging
import sys
from datetime import datetime
import os
import time


def countdown(n):
    """
    Prints a countdown from n to 0 in the console, updating the same line every second.

    Args:
        n (int): The starting number for the countdown.
    """
    for i in range(n, 0, -1):
        print(f"\r{i}", end="", flush=True)
        time.sleep(1)
    print("\r0", flush=True)  # Ensure the last number is also printed on the same line


def write_text_to_file(
    filepath: str,
    mode: str,
    text: str,
    separator_sign="=",
    separator_length=300,
    encoding="utf-8",
    add_time_stamp=True,
) -> bool:
    """
    Writes text to a file with optional timestamp and separator.

    Args:
        filepath (str): The path to the file.
        mode (str): The file opening mode, e.g., 'w' for write, 'a' for append.
        text (str): The text to write to the file.
        separator_sign (str): The character to use for the separator line.
        separator_length (int): The length of the separator line.
        encoding (str): The file encoding.
        add_time_stamp (bool): Whether to add a timestamp to the text.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        # Ensure the directory exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        seperator = separator_length * separator_sign
        with open(filepath, mode, encoding=encoding) as file:
            if add_time_stamp:
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                file.write(f"({timestamp}) -> {text}\n")
            else:
                file.write(f"{text} \n")
            if seperator:
                file.write(seperator + "\n")
        return True
    except Exception as e:
        print("An error occurred: ", e)
        return False


def get_logger() -> logging.Logger:
    """
    Get a logger instance configured for logging to stdout.

    Returns:
        logging.Logger: A logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)

    return logger


def get_formatted_date_time_now() -> str:
    # Get the current date and time
    now = datetime.now()

    # Format the date and time
    formatted_date_time = now.strftime("%d/%m/%Y %H:%M")

    # Print the formatted date and time
    return formatted_date_time


def retry_function(func, role_name, max_attempts=3, delay=1.0, backoff=1, *args, **kwargs):
    """
    Retry a function for a specified number of attempts.

    Parameters:
    - func: The function to be retried.
    - max_attempts: Maximum number of attempts.
    - delay: Initial delay between attempts in seconds.
    - backoff: Multiplier for the delay between attempts.
    - args, kwargs: Arguments to pass to the function being retried.

    Returns:
    - The result of the function call if successful.
    """
    attempt = 0
    current_delay = delay

    while attempt < max_attempts:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"({role_name}) -> Attempt {attempt + 1} failed: {e}")
            attempt += 1
            if attempt < max_attempts:
                time.sleep(current_delay)
                current_delay *= backoff
            else:
                return None

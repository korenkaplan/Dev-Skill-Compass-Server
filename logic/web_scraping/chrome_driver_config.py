"""This Module is responsible for initialzing the webdriver service with chrome Options"""
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

chrome_headless_arguments = ('--headless', '--no-sandbox', '--disable-dev-shm-usage',
                             "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                             " (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_arguments = ('--no-sandbox', '--disable-dev-shm-usage')


def initialize_headless_chrome_driver(arguments=chrome_arguments) -> tuple[Service, Options]:
    """Function to initialize the headless chrome driver"""
    # Setup Chrome options
    chrome_options = Options()

    # Add default arguments if not provided
    for argument in arguments:
        chrome_options.add_argument(argument)

    # Set path to chromedriver as per your configuration
    webdriver_service = Service("C:\\Users\\Koren Kaplan\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")

    # return the chrome_options and the webdriver_service
    return webdriver_service, chrome_options

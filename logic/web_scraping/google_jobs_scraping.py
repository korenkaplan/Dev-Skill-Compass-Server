""" this module is dedicated to script job listings from google jobs"""
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException
from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import DriverManager
from decorators import messure_function_time_dec


# region constants
# Define the GoogleJobsTimePeriod Enum
class GoogleJobsTimePeriod(Enum):
    TODAY = 'today'
    THREE_DAYS = '3days'
    WEEK = 'week'
    MONTH = 'month'


# def click_button(xpath, driver):
#     try:
#         button = show_full_desc_button = driver.find_element(By.XPATH, xpath)
#         button.click()
#         return True
#     except Exception as e:
#         print(e)
#         return False
def click_button(xpath, _driver, timeout=1.0) -> bool:
    try:
        # Wait for the button to be present in the DOM
        button = WebDriverWait(_driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

        # Once present, wait for it to be clickable
        WebDriverWait(_driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

        # Click the button
        button.click()
        return True
    except TimeoutException as e:
        error = f"Timed out waiting for button to be present or clickable: {e}"
        write_text_to_file('click_button_logs.txt', 'a', error, 400 * "=")
        return False
    except NoSuchElementException as e:
        error = f"Button not found: {e}"
        write_text_to_file('click_button_logs.txt', 'a', error, 400 * "=")
        return False
    except ElementClickInterceptedException as e:
        error = f"Button click intercepted: {e}"
        write_text_to_file('click_button_logs.txt', 'a', error, 400 * "=")
        return False
    except Exception as e:
        error = f"An error occurred: {e}"
        write_text_to_file('click_button_logs.txt', 'a', error, 400 * "=")
        return False


def get_full_description(xpath, _driver):
    try:
        # Wait for the element to be present in the DOM
        element = WebDriverWait(_driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException as e:
        print("Timed out waiting for element to be present:", e)
    try:
        # Once present, wait for it to be visible
        WebDriverWait(_driver, 10).until(EC.visibility_of(element))
    except TimeoutException as e:
        print("Timed out waiting for element to be visible:", e)

    try:
        # Retrieve and return the text of the element
        description = element.text
        if description:
            return description
        else:
            print("Element is present but contains no text.")
    except Exception as e:
        print("An error occurred:", e)


def write_text_to_file(filepath, mode, text, seperator, encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as file:
        file.write(text + '\n')
        if seperator:
            file.write(seperator + '\n')


# region params
# Define the search key and time period
search_key = 'backend developer'.replace(' ', '+')
time_period = GoogleJobsTimePeriod.MONTH.value
# Construct the base URL
base_url = (f"""
https://www.google.com/search?q={search_key}+jobs+israel&ibp=htl;jobs&hl=en&gl=us#fpstate=tldetail&=&=&htivrt=jobs&htichips=date_posted:{time_period}&htischips=date_posted;{time_period}&htidocid=nPmFkUrgbES8cLN1AAAAAA%3D%3D
""")
print(base_url)

params = {
    "latitude": 32.109333,
    "longitude": 34.855499,
    "accuracy": 100
}
# Set up the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
driver.get(base_url)


wait = WebDriverWait(driver, 10)
button_full_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/div/div/div/div/g-expandable-content/span/div/g-inline-expansion-bar/div[1]/div'
expandable_text_full_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/div/span'
text_full_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/span'
# endregion



# Wait for the job listings to appear
try:
    job_listings = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "li")))
except TimeoutException:
    print("Job listings did not appear within the timeout period.")
    driver.quit()
    exit()

print('total: ', len(job_listings))

skip_amount = 0
previous_size = -1
inserted_descriptions = 0
button_not_found_count = 0
while job_listings:
    # If the previous size is the same as the current size, there are no more job listings to load
    if previous_size == len(job_listings):
        break

    previous_size = len(job_listings)
    # Iterate through each job listing, skipping the previously clicked ones
    for i in range(skip_amount, len(job_listings)):
        # Scroll to view
        driver.execute_script("arguments[0].scrollIntoView();", job_listings[i])
        # Click on the listing
        job_listings[i].click()

        try:
            is_clicked = click_button(button_full_xpath, driver, timeout=0.5)
            if is_clicked:
                description = get_full_description(expandable_text_full_xpath, driver)
            else:
                description = get_full_description(text_full_xpath, driver)
                button_not_found_count += 1

            if description:
                inserted_descriptions += 1
                write_text_to_file('descriptions.txt', 'a', description, 400 * "=")

        except NoSuchElementException:
            print("Target element not found!")

    # Update the skip amount for the next iteration
    skip_amount = len(job_listings)

    # Refind the job listings to avoid StaleElementReferenceException
    job_listings = driver.find_elements(By.CSS_SELECTOR, "li")
print(f"Inserted descriptions: {inserted_descriptions}, job_listings:{len(job_listings)}, button not found: {button_not_found_count}")

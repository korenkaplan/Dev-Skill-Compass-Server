""" this module is dedicated to script job listings from google jobs"""
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
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


# region constants
# Define the GoogleJobsTimePeriod Enum
class GoogleJobsTimePeriod(Enum):
    TODAY = 'today'
    THREE_DAYS = '3days'
    WEEK = 'week'
    MONTH = 'month'


# region params
# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")

# Set location to Israel
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US',
                                                 'profile.default_content_setting_values.geolocation': 2})
# Define the search key and time period
search_key = 'backend developer'.replace(' ', '+')
time_period = "month"
# Construct the base URL
base_url = f"""https://www.google.com/search?q=backend+developer+israel&ibp=htl;jobs&hl=en&gl=us#fpstate=tldetail&htivrt=jobs&htidocid=HUMxCwC4tTSqEtNyAAAAAA%3D%3D"""

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

#
# # endregion
# button_xpath = '//*[@id="_yNtVZtziFeOqkdUPtYyw4A8_6"]'
# button_full_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/div/div/div/div/g-expandable-content/span/div/g-inline-expansion-bar/div[1]/div'
# expandable_text_full_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/div/span'
# text_full_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/span'
# text_xpath = '//*[@id="gws-plugins-horizon-jobs__job_details_page"]/div/div[4]/g-expandable-container/div/div/span'
# wait = WebDriverWait(driver, 10)


def click_button(xpath, _driver) -> bool:
    try:
        # Wait for the button to be present in the DOM
        button = WebDriverWait(_driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

        # Once present, wait for it to be clickable
        WebDriverWait(_driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))

        # Click the button
        button.click()
        return True
    except TimeoutException as e:
        print("Timed out waiting for button to be present or clickable:", e)
        return False
    except NoSuchElementException as e:
        print("Button not found:", e)
        return False
    except ElementClickInterceptedException as e:
        print("Button click intercepted:", e)
        return False
    except Exception as e:
        print("An error occurred:", e)
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


def get_span_text(url, xpath):
  response = requests.get(url)
  if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'lxml')
    # Check for successful parsing
    if soup.title:
      dom = etree.HTML(str(soup))
      element = dom.xpath(xpath)
      if element:
        return element[0].text
      else:
        return "Element not found"
    else:
      return "Failed to parse HTML content"
  else:
    return f"Failed to retrieve the page. Status code: {response.status_code}"



button_xpath = '//*[@id="_yNtVZtziFeOqkdUPtYyw4A8_6"]'
button_full_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/div/div/div/div/g-expandable-content/span/div/g-inline-expansion-bar/div[1]/div'
expandable_text_full_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/div/span'
text_full_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/g-expandable-container/div/div/span'
text_xpath = '//*[@id="gws-plugins-horizon-jobs__job_details_page"]/div/div[4]/g-expandable-container/div/div/span'

print(get_full_description(text_full_xpath, driver))
# print(get_span_text(base_url, text_full_xpath))

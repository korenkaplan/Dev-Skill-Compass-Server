"""
listings_list = get_job_listings(config_object.search_value, driver, wait,
                                         config_object.show_full_description_button_xpath,
                                         config_object.expandable_job_description_text_xpath,
                                         config_object.log_file_path,
                                         config_object.not_expandable_job_description_text_xpath, click_button_timeout)
"""
from pydantic import BaseModel
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class GoogleJobsGetJobListingsDto(BaseModel):
    role: str
    driver: WebDriver
    wait: WebDriverWait
    expand_job_description_button_xpath: str
    expandable_job_description_xpath: str
    log_file_path: str
    not_expanded_job_description_xpath: str
    click_button_timeout: float = 1.0

    class Config:
        arbitrary_types_allowed = True

from pydantic import BaseModel
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class LinkedinGetJobListingsDto(BaseModel):
    role: str
    driver: WebDriver
    wait: WebDriverWait
    result_list_xpath: str
    description_div_xpath: str
    show_more_button_xpath: str
    see_more_jobs_btn_xpath: str

    class Config:
        arbitrary_types_allowed = True

"""
Dto for the function that finds the title element
"""
from pydantic import BaseModel
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class GoogleJobsTitleElementXpathDto(BaseModel):
    wait: WebDriverWait
    listing_li_element: WebElement
    increase_every_ten: int
    one_to_ten: int
    only_first_is_one_else_2: int
    extra_div: str
    is_wait: bool

    class Config:
        arbitrary_types_allowed = True

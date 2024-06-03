"""
Dto for getting the job description of a listing in google jobs
"""

from pydantic import BaseModel
from selenium.webdriver.chrome.webdriver import WebDriver


class GoogleJobsGetFullDescriptionDto(BaseModel):
    driver: WebDriver
    expand_job_description_button_xpath: str
    expandable_job_description_xpath: str
    not_expanded_job_description_xpath: str
    click_button_timeout: int
    log_file_path: str

    class Config:
        arbitrary_types_allowed = True

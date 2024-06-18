""" this module is responsible for building the url for the LinkedIn scraping process"""
from utils.enums import LinkedinTimePeriod


def format_role(role: str, seperator="%2B") -> str:
    # replace spaces with the seperator
    return role.replace(' ', seperator).lower()


def build_url(role_name: str, period: LinkedinTimePeriod):
    # format the role name to the url format
    formated_role: str = format_role(role_name)

    if period == LinkedinTimePeriod.ALL_TIME:
        return (f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={formated_role}&"
                f"location=Israel&geoId=101620260&start=")

    return (f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={formated_role}&"
            f"location=Israel&geoId=101620260&f_TPR={period.value}&start=")

# region WSGI
"""
WSGI config for django_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")

application = get_wsgi_application()
# endregion
from logic.web_scraping.main_scrape_file import job_scrape_pipeline
from utils.enums import GoogleJobsTimePeriod, LinkedinTimePeriod


job_scrape_pipeline('backend developer', GoogleJobsTimePeriod.MONTH, LinkedinTimePeriod.ALL_TIME)


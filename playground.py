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
from logic.web_scraping.main_scrape_file import job_scrape_pipeline, job_scrape_pipeline_test
from utils.enums import GoogleJobsTimePeriod, LinkedinTimePeriod
from usage_stats.management.commands.run_daily_pipeline import daily_pipeline
from datetime import datetime
import requests

# job_scrape_pipeline_test('backend developer', LinkedinTimePeriod.PAST_MONTH)

res = requests.get('http://127.0.0.1:8000//core/get_jobs_count_for_role/?role_id=55')
print(res.content)

# region WSGI
"""
WSGI config for django_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
from logic.web_scraping.google_jobs.google_jobs_scraping import is_title_in_synonyms_words

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")

application = get_wsgi_application()
# endregion

from usage_stats.models import MonthlyTechnologiesCounts, AggregatedTechCounts, HistoricalTechCounts
from logic.pipelines.weekly_pipeline import weekly_pipeline
from core.models import Roles, Technologies
from logic.pipelines.main import process_pool_role_pipline_test




def print_python_backend(tech, role):
    backend_role = Roles.objects.filter(name=role).first()
    python = Technologies.objects.filter(name=tech).first()
    python_backend_count = AggregatedTechCounts.objects.filter(role_id=backend_role, technology_id=python)
    print(python_backend_count)





if __name__ == '__main__':
    process_pool_role_pipline_test(GoogleJobsTimePeriod.MONTH)
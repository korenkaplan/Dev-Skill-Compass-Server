# region WSGI
"""
WSGI config for django_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from collections import defaultdict

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")

application = get_wsgi_application()
# endregion
# region Imports
from core.services.roles_service import get_top_categories_for_role
from logic.pipelines.weekly_pipeline import weekly_pipeline, weekly_pipeline_test
from logic.pipelines.monthly_pipeline import monthly_pipeline
from django.core.management.base import BaseCommand
from init_db.init_database_functions import initialize_pipeline
from init_db.data.data import get_tech_dict, get_roles_dict
from core.models import Roles, Technologies, Synonyms, Categories
from usage_stats.models import MonthlyTechnologiesCounts, HistoricalTechCounts, AggregatedTechCounts
from logic.pipelines.main import thread_pool_role_pipline_test, thread_pool_role_pipline
from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
from logic.web_scraping.main_scrape_file import job_scrape_pipeline
import json
from core.serializers import RoleSerializer
from usage_stats.services.aggregated_tech_counts_service import get_role_count_stats
from dotenv import load_dotenv
import os


load_dotenv()

# endregion
# region Find Categories with most items
# res = AggregatedTechCounts.objects.filter(role_id__name='qa engineer').order_by('-counter')
# dictionary = defaultdict(int)
# for item in res:
#     if item.technology_id.category_id.name in dictionary.keys():
#         dictionary[item.technology_id.category_id.name] += 1
#     else:
#         dictionary[item.technology_id.category_id.name] = 1
#
# for k, v in dictionary.items():
#     if v > 6:
#         print(k)
# endregion
# region Test Email
# to = os.environ.get('EMAIL_HOST_USER')
# website_name = 'Google Jobs'
# date_and_time = get_formatted_date_time_now()
# text = """
# Backend Developer: 125
# Frontend Developer: 125
# Devops Developer: 125
# Data Analyst: 125
# QA Engineer: 125
# --------------------
# Total: 625
# """
# send_scan_recap_email(to, website_name, date_and_time, text)
# endregion


thread_pool_role_pipline(GoogleJobsTimePeriod.TODAY)


def clear_db():
    MonthlyTechnologiesCounts.objects.all().delete()
    HistoricalTechCounts.objects.all().delete()
    AggregatedTechCounts.objects.all().delete()
    Synonyms.objects.all().delete()
    Technologies.objects.all().delete()
    Categories.objects.all().delete()
    Roles.objects.all().delete()



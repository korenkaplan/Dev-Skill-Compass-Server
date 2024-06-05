# # region WSGI
# """
# WSGI config for django_server project.
#
# It exposes the WSGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
# """
#
# import os
#
# from django.core.wsgi import get_wsgi_application
#
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")
#
# application = get_wsgi_application()
# # endregion
#
#
# from logic.pipelines.weekly_pipeline import weekly_pipeline, weekly_pipeline_test
# from logic.pipelines.monthly_pipeline import monthly_pipeline
# from django.core.management.base import BaseCommand
# from init_db.init_database_functions import initialize_pipeline
# from init_db.data.data import get_tech_dict, get_roles_dict
# from core.models import Roles, Technologies, Synonyms, Categories
# from usage_stats.models import MonthlyTechnologiesCounts, HistoricalTechCounts, AggregatedTechCounts
# from logic.pipelines.main import thread_pool_role_pipline_test
# from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
# from logic.web_scraping.main_scrape_file import job_scrape_pipeline
# from usage_stats.services.aggregated_tech_counts_service import get_top_counts_for_role,
# get_top_counts_for_all_roles, \
#     get_last_scan_date_and_time
# import json
#
# # tech_dict = get_tech_dict()
# # roles = get_roles_list()
# # res_message = initialize_pipeline(tech_dict, roles)
#
#
# def clear_db():
#     MonthlyTechnologiesCounts.objects.all().delete()
#     HistoricalTechCounts.objects.all().delete()
#     AggregatedTechCounts.objects.all().delete()
#     Synonyms.objects.all().delete()
#     Technologies.objects.all().delete()
#     Categories.objects.all().delete()
#     Roles.objects.all().delete()
#
#
# res = get_last_scan_date_and_time()
#
# print(json.dumps(res, indent=4))

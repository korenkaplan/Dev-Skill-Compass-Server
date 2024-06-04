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
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")
#
# application = get_wsgi_application()
# # endregion
#
# from usage_stats.models import MonthlyTechnologiesCounts, AggregatedTechCounts, HistoricalTechCounts
# from logic.pipelines.weekly_pipeline import weekly_pipeline
# from core.models import Roles, Technologies, Synonyms
# from logic.pipelines.main import process_pool_role_pipline_test, get_all_techs_from_db
# from init_db.data.data import get_tech_set
# from logic.text_analysis.tech_term_finder import find_tech_terms
# from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
# from logic.web_scraping.google_jobs.google_jobs_scraping import is_title_in_synonyms_words
#
#
# # process_pool_role_pipline_test(GoogleJobsTimePeriod.MONTH)
#
# res = MonthlyTechnologiesCounts.objects.filter(role_id__name="Backend Developer").order_by('-counter')
#
# for item in res:
#     print(item)

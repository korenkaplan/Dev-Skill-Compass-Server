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
# from logic.pipelines.weekly_pipeline import weekly_pipeline, weekly_pipeline_test
# from logic.pipelines.monthly_pipeline import monthly_pipeline
# from django.core.management.base import BaseCommand
# from init_db.init_database_functions import initialize_pipeline
# from init_db.data.data import get_tech_dict, get_roles_list
# from core.models import Roles, Technologies, Synonyms, Categories
# from logic.pipelines.main import process_pool_role_pipline_test
# from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
#
# # tech_dict = get_tech_dict()
# # roles = get_roles_list()
# # res_message = initialize_pipeline(tech_dict, roles)
#
#
#
#
# # Synonyms.objects.all().delete()
# # Technologies.objects.all().delete()
# # Categories.objects.all().delete()
# # q = Roles.objects.all().first()
# #
# # res = [category for category in q.categories.all()]
# # print(q.categories.all())
#

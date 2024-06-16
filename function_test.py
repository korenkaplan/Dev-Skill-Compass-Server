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
from logic.pipelines.main import thread_pool_role_pipline, thread_pool_role_pipline_test
from utils.enums import GoogleJobsTimePeriod
from utils.enums import LinkedinTimePeriod
from init_db.data.data import get_roles_dict, get_tech_dict
from init_db.init_database_functions import initialize_pipeline
from playground import clear_db
from usage_stats.models import MonthlyTechnologiesCounts

# clear_db()
# tech_dict = get_tech_dict()
# roles = get_roles_dict()
# initialize_pipeline(tech_dict, roles)
thread_pool_role_pipline_test(GoogleJobsTimePeriod.WEEK, LinkedinTimePeriod.PAST_WEEK)

res = MonthlyTechnologiesCounts.objects.filter(role_id__name="qa engineer")
print(res)


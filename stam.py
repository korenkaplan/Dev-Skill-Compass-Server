# region WSGI
"""
WSGI config for django_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.db.models import Sum

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")

application = get_wsgi_application()
# endregion

from usage_stats.models import MonthlyTechnologiesCounts, AggregatedTechCounts, HistoricalTechCounts
from logic.pipelines.weekly_pipeline import weekly_pipeline
from core.models import Roles, Technologies


def print_python_backend(tech, role):
    backend_role = Roles.objects.filter(name=role).first()
    python = Technologies.objects.filter(name=tech).first()
    python_backend_count = AggregatedTechCounts.objects.filter(role_id=backend_role, technology_id=python)
    print(python_backend_count)


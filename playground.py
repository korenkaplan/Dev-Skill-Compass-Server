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
from usage_stats.models import MonthlyTechnologiesCounts
from datetime import datetime
# endregion
filterDate = datetime(2024, 8, 1)

technology_counts = MonthlyTechnologiesCounts.objects.all()
print(len(technology_counts))

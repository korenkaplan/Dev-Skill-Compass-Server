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

from usage_stats.models import MonthlyTechnologiesCounts
from dateutil.relativedelta import relativedelta
from django.utils import timezone
number_of_months = 2
today = timezone.now()
past_date = today - relativedelta(days=2)


rows = MonthlyTechnologiesCounts.objects.filter(created_at__gt=past_date)

for row in rows:
    print(row)

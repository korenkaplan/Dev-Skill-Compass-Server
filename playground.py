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
from usage_stats.services.aggregated_tech_counts_service import get_role_count_stats


role_id = 59
items = get_role_count_stats(role_id, number_of_categories=6)

for key, value in items.items():
    print(value)

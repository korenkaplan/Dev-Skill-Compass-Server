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
from usage_stats.management.commands.run_daily_pipeline import daily_pipeline
from utils.functions import retry_function

# Call your initialization function here
retry_function(daily_pipeline, role_name='daily_pipeline')
# process_pool_role_pipline()
print("run_daily_pipeline command executed")

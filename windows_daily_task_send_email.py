# region WSGI
"""
WSGI config for django_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from usage_stats.management.commands.email_test_command import test_send_email, daily_test

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")

application = get_wsgi_application()

# endregion
from utils.functions import retry_function

# Call your initialization function here
retry_function(test_send_email, role_name='test_send_email')
retry_function(daily_test, role_name='daily_test')
# process_pool_role_pipline()
print("test_send_email command executed")

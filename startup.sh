#!/bin/bash
python manage.py collectstatic && gunicorn --workers 2 django_server.wsgi
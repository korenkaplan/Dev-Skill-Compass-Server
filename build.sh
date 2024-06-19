#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

python manage.py migrate &&
python manage.py crontab add &&
cron


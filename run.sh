#!/bin/bash

# 1. Run migrations (always good to automate this)
# python manage.py migrate --noinput

# 2. Run your custom admin setup command
# python manage.py setup_admin

# 3. Start the actual web server (Gunicorn)
exec gunicorn django_project.wsgi:application --bind 0.0.0.0:8000
#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --run-syncdb
python manage.py clear_scripts_running_status

daphne -b 0.0.0.0 -p 8080 dqmhelper.asgi:application

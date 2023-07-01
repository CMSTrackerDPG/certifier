#!/bin/bash
echo "188.184.88.153 login.cern.ch" >> /etc/hosts

python manage.py collectstatic --noinput
python manage.py migrate --run-syncdb
python manage.py clear_scripts_running_status

daphne -b 0.0.0.0 -p 8080 dqmhelper.asgi:application

#!/bin/bash

python manage.py collectstatic --noinput
python manage.py migrate --run-syncdb

daphne -b 0.0.0.0 -p 8080 dqmhelper.asgi:application

#!/bin/bash

python manage.py collectstatic --noinput

daphne dqmhelper.asgi:application -u /sock/daphne.sock -b 0.0.0.0 -p 8080


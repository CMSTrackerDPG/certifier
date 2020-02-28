#!/bin/bash

python manage.py collectstatic --noinput

daphne -b 127.0.0.1 -p 8080 dqmhelper.asgi:application

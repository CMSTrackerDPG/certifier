#!/bin/bash

python manage.py collectstatic --noinput

daphne -u /sock/daphne.sock dqmhelper.asgi:application


#!/bin/bash

python manage.py collectstatic --noinput

daphne dqmhelper.asgi:application -u /sock/daphne.sock


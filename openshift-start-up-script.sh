#!/bin/bash

python manage.py makemigrations --noinput

python manage.py migrate --noinput

daphne dqmhelper.asgi:application -u /tmp/daphne.sock


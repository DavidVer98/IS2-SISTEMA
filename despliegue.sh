#!/bin/bash

./config.sh

source venv/bin/activate

./manage.py loaddata archivo.json

./manage.py makemigrations

./manage.py migrate

./manage.py runserver
#!/bin/bash

./config.sh

./manage.py loaddata archivo.json

./manage.py makemigrations

./manage.py migrate

./manage.py runserver
#!/bin/bash

./config.sh

./manage.py loaddata archivo.json

./manage.py makemigrations

./manage.py migrate

/usr/bin/firefox -new-window http://127.0.0.1:8080
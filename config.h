#!/bin/bash

sudo -u postgres psql -f db.sql

sudo find -name [000]*_initial.py | grep -v venv | xargs rm -f

source venv/bin/activate

./manage.py makemigrations

./manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')" | python manage.py shell



#!/bin/bash

sudo -u postgres psql -f db.sql

sudo find -name [000][0-9]*_*.py | grep -v venv | xargs rm -f

python3.9 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

./manage.py makemigrations

./manage.py migrate

echo yes | ./manage.py collectstatic

cat djangoconfig.txt | python manage.py shell

sudo ./produccion.sh

/usr/bin/firefox -new-window http://127.0.0.1:8080



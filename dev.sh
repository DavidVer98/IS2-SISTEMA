#!/bin/bash

git clone git@github.com:DavidVer98/IS2-SISTEMA.git

cd IS2-SISTEMA

python3.9 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

pip install django gunicorn psycopg2-binary

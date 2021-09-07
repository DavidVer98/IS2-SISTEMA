#!/bin/bash

git clone git@github.com:DavidVer98/IS2-SISTEMA.git

# opcional

cd IS2-SISTEMA || exit

python3.9 -m venv venv

source venv/bin/activate

pip install -r requirements.txt



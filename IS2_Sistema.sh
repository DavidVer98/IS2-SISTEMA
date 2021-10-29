#!/bin/bash

git clone git@github.com:DavidVer98/IS2-SISTEMA.git

cd IS2-SISTEMA

TAG=$(git describe --tags $(git rev-list --tags --max-count=1))

./tags.sh $TAG

./despliegue.sh


#!/bin/bash

echo 'iteraciones:'

git tag

echo 'Ingrese iteracion al cual se desea cambiar'

read iteracion

: $(git -c credential.helper= -c core.quotepath=false -c log.showSignature=false checkout $iteracion)
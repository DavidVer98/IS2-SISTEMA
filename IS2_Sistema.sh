#!/bin/bash

git clone git@github.com:DavidVer98/IS2-SISTEMA.git

cd IS2-SISTEMA

echo "Elegir entorno (produccion o desarrollo)"

read rama

echo $rama

if [ "$rama" = "desarrollo" ]; then
	echo "Elegir tag"
	git tag | grep -v _produccion
	read TAG
elif [ "$rama" = "produccion" ]; then
	echo "Elegir tag"
	git tag | grep _produccion
	read TAG
else 
	echo "ingreso una rama equivocada, por defecto estara en la rama main"
fi

#TAG=$(git describe --tags $(git rev-list --tags --max-count=1))

./tags.sh $TAG


if [[ $TAG == *"5"* || $TAG == *"6"* ]]; then

	./despliegue.sh
fi



# IS2-Sistema de Gestión de Proyectos


## Integrantes ✒️


* **David Veron** -  - [DavidVer98](https://github.com/villanuevand)
* **Elias Recalde** -  - [recaldelias](https://github.com/recaldelias)
* **Alexis Cubilla** -  - [AlexisCubilla](https://github.com/AlexisCubilla)
* **Nicholas Jara** -  - [AdmsAlf](https://github.com/AdmsAlf)


## Características 🛠️

- Django 3.0+
- Soporte de base de datos PostgreSQL con psycopg2.
- Bootstrap -v 5.1.0

## Requisitos (requisitos previos) 🚀

_Primero clone el repositorio de Github:_

```
$ git clone https://github.com/DavidVer98/IS2-SISTEMA.git
$ cd {{ project_name }}
```

_Active el virtualenv para su proyecto._
_Instale las dependencias del proyecto:_

```
(env) $ pip install -r requirements.txt
```

_Luego simplemete aplique las migraciones:_
```
(env) $ python manage.py migrate
```
_Ahora puede ejecutar el servidor de desarrollo:_
```
(env) $ python manage.py migrate
```
---

## Iniciar el servidor

_Introducir el siguiente scrip en la terminal:_
```
(env) $ python manage.py runserver
```
Ahora necesitas revisar que tu website se está ejecutando. Abre tu navegador (Firefox, Chrome, Safari, Internet Explorer, o cualquiera que uses) y escribe esta dirección:
```
 http://127.0.0.1:8000/
```
Con este ulripo paso ya podras ejecutar el sistema localmente



## El archivo `` test_views.py ''


Además del contenido de configuración común, el archivo `` test_views.py '' proporciona un enlace para ejecutar el conjunto de pruebas de la aplicación:

```
...
import unittest

def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)
```


Lo que permite ejecutar las pruebas con el argumento del comando de prueba:
```
    $ python manage.py test
```
---



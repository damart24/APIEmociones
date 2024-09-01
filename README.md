# Proyecto X

Este proyecto requiere Python y algunas dependencias adicionales. Para facilitar la instalación, todo lo que necesitas hacer es ejecutar un archivo `.bat` que se encargará de todo el proceso.

## Requisitos previos

- **Sistema operativo Windows**
- **Python 3.9.13** (se instalará automáticamente si no está presente)
- **Conexión a Internet** (para descargar Python y las dependencias)

## Instrucciones de instalación

Sigue estos pasos para instalar Python y todas las dependencias necesarias:

1. Clona este repositorio o descarga el código fuente.
2. Navega hasta la carpeta del proyecto.
3. Ejecuta el archivo `install.bat` (haz doble clic sobre él).

El archivo `install.bat` hará lo siguiente:

- Verificará si Python está instalado.
- Si Python no está instalado, descargará e instalará Python 3.9.13.
- Añadirá Python al PATH automáticamente.
- Instalará `pip` si no está presente.
- Instalará todas las dependencias listadas en el archivo `requirements.txt`.

### Nota

- Asegúrate de ejecutar el archivo `.bat` con permisos de administrador si es necesario.
- El proceso de instalación puede tomar unos minutos dependiendo de la velocidad de tu conexión a Internet.
- Es necesario que se encuentre el instador de python `python-3.9.13-amd64` y el `requirements.txt` en la misma carpeta que el `installer.bat`

## Uso

Una vez completada la instalación, puedes ejecutar el proyecto usando Python con el siguiente comando:
- Abrir la consola
- Hay que setear el proyecto en donde se encuentre el script del servidor como pudiese ser: set FLASK_APP=APIAnalisis\FlaskServer.py
- Hay que poner la consola en el path donde se encuentren por ejemplo: cd APIAnalisis
- Finalmente ejecuta flask run

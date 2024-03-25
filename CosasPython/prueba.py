# La función hello_world() está decorada con @app.route("/"), 
# lo que significa que esta función será llamada cuando alguien acceda 
# a la ruta raíz (/) de tu aplicación Flask.
# La función upload_wav() maneja la carga de archivos WAV 
# y está decorada con @app.route("/upload", methods=["POST"]), lo que significa que esta función
# será llamada cuando alguien envíe una solicitud POST a la ruta /upload.
# La función copyWavVersion() es llamada dentro de hello_world(), 
# y el resultado se muestra como parte de la respuesta HTML generada por esta función.
# Con esta configuración, cuando accedas a la ruta raíz de tu aplicación Flask 
# (por ejemplo, http://127.0.0.1:5000/), verás el mensaje generado por hello_world(), 
# que incluirá el resultado de copyWavVersion().

from flask import Flask, request
from HumePrueba import copyWavVersion, copyWavFromBytes

app = Flask(__name__)
print(__name__)

@app.route("/", methods=["POST"])
def upload_wav():
    archivo = request.files['file']
    # Lee los primeros 12 bytes del archivo
    header = archivo.read()
    
   
    # Reinicia el cursor del archivo para que pueda leerse de nuevo desde el principio
    archivo.seek(0)

    print(len(header))
    copyWavFromBytes(header)
    # Verifica si los primeros cuatro bytes son 'RIFF', que es la firma de un archivo WAV
    if header[:4] == b'RIFF':
        return 'WAV'
    else:
        return 'Tipo de archivo desconocido'




    # Verificar si se envió un archivo
    if 'file' not in request.files:
        return 'No se envió ningún archivo', 400

    file = request.files['file']

    print(type(file))
    # Verificar si no se envió ningún archivo
    if file.filename == '':
        return 'Nombre de archivo vacío', 400

    # Verificar si el archivo es un archivo WAV
    if file and file.filename.endswith('.wav'):
        # Guardar el archivo en el servidor
        file.save(file.filename)

        # Realizar alguna operación con el archivo WAV, como procesamiento o almacenamiento

        return 'Archivo WAV subido exitosamente ' + file.filename + ' ', 200

    return 'Tipo de archivo no soportado. Por favor, sube un archivo WAV', 400

@app.route("/")
def hello_world():
    result = copyWavVersion()
    return f"<p>Hello, World! Result: {result}</p>"

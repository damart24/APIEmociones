import base64
import io
import os
import asyncio
import pprint
import wave

from hume import HumeStreamClient
from hume.models.config import ProsodyConfig


def copyWavVersion():
    # Obtener la ruta del directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Conseguimos el path junto con el nombre donde se copiará el WAV
    WAVE_COPY_FILENAME = "Copia.wav"
    copyVersion_path = os.path.join(script_dir, WAVE_COPY_FILENAME)

    # Conseguimos el path junto con el nombre de donde sacaremos el WAV
    WAVE_ORIGINAL_FILENAME = "Original.wav"
    originalVersion_path = os.path.join(script_dir, WAVE_ORIGINAL_FILENAME)

    # Abrimos ambos archivos, el de copia solo de escritura, y el original solo de lectura
    copyVersionInstance = wave.open(copyVersion_path, 'wb')
    originalVersionInstance = wave.open(originalVersion_path, 'rb')

    # Copiamos las características del WAV original
    # print(originalVersionInstance.getnchannels())
    # print(originalVersionInstance.getsampwidth())
    # print(originalVersionInstance.getframerate())

    copyVersionInstance.setnchannels(originalVersionInstance.getnchannels())
    copyVersionInstance.setsampwidth(originalVersionInstance.getsampwidth())
    copyVersionInstance.setframerate(originalVersionInstance.getframerate())

    # Leemos los chunks hasta que no queden más, es decir el audio entero
    chunk_size = 1024  # Tamaño del chunk en frames
    chunk = originalVersionInstance.readframes(chunk_size)

    while chunk:
        copyVersionInstance.writeframes(chunk)
        chunk = originalVersionInstance.readframes(chunk_size)


    copyVersionInstance.close()
    originalVersionInstance.close()
    # Se ejecuta el resultado final enviándolo y analizando el audio
    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_file(copyVersion_path)
            #pprint.pprint(result)

    asyncio.run(main())
    return "Funcionaaaaa"

# Crea un wav a partir de los bytes y devuelve nchannels, samwidth y framerate
def obtener_caracteristicas_wav_desde_bytes(bytes_wav):
    # Crear un objeto de archivo WAV a partir de los bytes
    wav_file = wave.open(io.BytesIO(bytes_wav))

    # Obtener características del archivo WAV
    n_channels = wav_file.getnchannels()
    sampwidth = wav_file.getsampwidth()
    framerate = wav_file.getframerate()

    # Cerrar el archivo WAV
    wav_file.close()

    return n_channels, sampwidth, framerate

# Mirar si puedo saber las características del wav
def copyWavFromBytes(bytesFromWav):
    print(bytesFromWav[:44])
    # Obtener características del archivo WAV desde los bytes
    n_channels, sampwidth, framerate = obtener_caracteristicas_wav_desde_bytes(bytesFromWav)

    # Imprimir las características obtenidas
    print("Número de canales:", n_channels)
    print("Ancho de muestra (en bytes):", sampwidth)
    print("Frecuencia de muestreo:", framerate)

    # Obtener la ruta del directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Conseguimos el path junto con el nombre donde se copiará el WAV
    WAVE_COPY_FILENAME = "CopiaBytes.wav"
    copyVersion_path = os.path.join(script_dir, WAVE_COPY_FILENAME)

    # Abrimos ambos archivos, el de copia solo de escritura, y el original solo de lectura
    copyVersionInstance = wave.open(copyVersion_path, 'wb')

    # Copiamos las características del WAV original
    copyVersionInstance.setnchannels(n_channels)
    copyVersionInstance.setsampwidth(sampwidth)
    copyVersionInstance.setframerate(framerate)

    copyVersionInstance.writeframes(bytesFromWav)

    copyVersionInstance.close()

    bytesFromWav_copy = base64.b64encode(bytesFromWav) 
    # Se ejecuta el resultado final enviándolo y analizando el audio
    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_bytes(bytesFromWav_copy)
            pprint.pprint(result)

    asyncio.run(main())
    return "FuncionaaaaaVersiónCopia"


def sendBytesDirectly(bytesFromWav):
    print(bytesFromWav[:44])
    bytesFromWav_copy = base64.b64encode(bytesFromWav) 
    # Se ejecuta el resultado final enviándolo y analizando el audio
    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_bytes(bytesFromWav_copy)
            pprint.pprint(result)

    asyncio.run(main())
    return "FuncionaaaaaVersiónCopia"


def sendBytesFromLoadedWav():
    # Obtener la ruta del directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Conseguimos el path junto con el nombre de donde sacaremos el WAV
    WAVE_ORIGINAL_FILENAME = "Original.wav"
    originalVersion_path = os.path.join(script_dir, WAVE_ORIGINAL_FILENAME)

    originalVersionInstance = wave.open(originalVersion_path, 'rb')

     # Leemos los bytes del archivo WAV original
    wav_bytes = originalVersionInstance.readframes(originalVersionInstance.getnframes())

    print(type(wav_bytes))
    

    wav_bytes64 = base64.b64encode(wav_bytes) 

    print(type(wav_bytes64))
    # Cerramos el archivo WAV original
    originalVersionInstance.close()
    # Se ejecuta el resultado final enviándolo y analizando el audio
    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_bytes(wav_bytes64)
            pprint.pprint(result)

    asyncio.run(main())
    return "No funciona"




# copyWavVersion()

# Obtener la ruta del directorio del script
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Conseguimos el path junto con el nombre de donde sacaremos el WAV
# WAVE_ORIGINAL_FILENAME = "Original.wav"
# originalVersion_path = os.path.join(script_dir, WAVE_ORIGINAL_FILENAME)



# originalVersionInstance = wave.open(originalVersion_path, 'rb')

# chunk = originalVersionInstance.readframes(44)


# copyWavFromBytes(chunk)
# sendBytesVersion()
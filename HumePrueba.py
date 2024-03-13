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
            pprint.pprint(result)

    asyncio.run(main())
    return "Funcionaaaaa"

def sendBytesVersion():
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
    return "Funcionaaaaa"


# sendBytesVersion()








# def version_final(
#         # path
#         ):
#     from pprint import pprint
#     import asyncio

#     from hume import HumeStreamClient
#     from hume.models.config import ProsodyConfig

   


#     async def main():
       
#         # client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
#         # config = ProsodyConfig()
#         # # async with client.connect([config]) as socket:
#         # #     result = await socket.send_file(path)
#         # #     pprint(result)

#     # asyncio.run(main())
#     # return "Siuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"
        




    


   
import base64
import io
import os
import asyncio
import pprint
import wave
import numpy as np

from hume import HumeStreamClient
from hume.models.config import ProsodyConfig
from scipy.io import wavfile

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

#Algoritmo de prueba donde cojo las 5 emociones mas predominantes
def algoritmoEmocionesBasicoPrueba(emotionsList):
    emotions = emotionsList['prosody']['predictions'][0]['emotions']
    top_5_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)[:5]

    for emotion in top_5_emotions:
        print(emotion['name'], emotion['score'])

    print("ESTOY ENTRANDO")

    return top_5_emotions

# Función para ordenar las emociones en cada categoría
def sort_emotions_by_category(emotions_by_category, emotions_dict):
    emotions_list = emotions_dict['prosody']['predictions'][0]['emotions']
    
    # Inicializar un diccionario para almacenar la suma de puntuaciones por categoría
    summed_emotions = {category: 0 for category in emotions_by_category}  
    
    for emotion in emotions_list:
        for category, category_emotions in emotions_by_category.items():
            if any(substring in emotion['name'] for substring in category_emotions):
                summed_emotions[category] += emotion['score']
    
    return summed_emotions
    
# import aubio
# def get_pitch(filename):
#     # Abre el archivo de audio
#     samplerate, data = aubio.source(filename)
    
#     # Crea el objeto de tono (pitch) de aubio
#     pitch_o = aubio.pitch("yin", samplerate)
#     pitch_o.set_unit("Hz")  # Configura la unidad de medida del tono en Hz
    
#     pitches = []  # Lista para almacenar los tonos detectados
    
#     # Procesa el audio
#     total_frames = 0
#     while True:
#         samples, read = data()
#         pitch = pitch_o(samples)[0]
#         confidence = pitch_o.get_confidence()
#         if confidence > 0.5:  # Considera solo tonos detectados con alta confianza
#             pitches.append(pitch)
#         total_frames += read
#         if read < hop_size:
#             break
    
#     return pitches

def get_wav_amplitudes(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        # Read all audio frames as byte data
        audio_data = wav_file.readframes(wav_file.getnframes())
        # Convert byte data to a numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        # Normalize the audio data to range [-1, 1]
        normalized_audio = audio_array / np.iinfo(audio_array.dtype).max
        # Calculate the average amplitude
        average_amplitude = np.mean(np.abs(normalized_audio))
    return average_amplitude



#Algoritmo donde se ordenan las emociones en 5 categorias
def algoritmoEmociones(emotionsList):
    # Definir el diccionario de emociones por categoría
    emotions_by_category = {
        'Felicidad': ['Admiration', 'Amusement', 'Contentment', 'Triumph', 'Determination',
                    'Adoration', 'Joy', 'Sympathy', 'Love', 'Excitement', 'Desire',
                    'Interest', 'Satisfaction', 'Romance', 'Surprise (positive)',
                    'Concentration', 'Ecstasy'],
        'Tristeza': ['Boredom', 'Distress', 'Disappointment', 'Tiredness', 'Sadness',
                     'Calmness', 'Nostalgia', 'Relief', 'Surprise (negative)'],
        'Miedo': ['Anxiety', 'Confusion', 'Tiredness', 'Awe', 'Embarrassment', 'Shame',
                'Doubt', 'Horror', 'Fear', 'Confusion', 'Empathic Pain', 'Contemplation'],
        'Asco': ['Awkwardness', 'Disgust', 'Craving', 'Pride', 'Aesthetic Appreciation'],
        'Enfado': ['Guilt', 'Annoyance', 'Anger', 'Contempt', 'Envy', 'Pain', 'Craving', 'Entrancement']
    }

    # Ordenar las emociones por categoría
    sorted_emotions_by_category = sort_emotions_by_category(emotions_by_category, emotionsList)

    return sorted_emotions_by_category

#Obtengo los bytes de un wav a partir de su nombre, en la ubicación 
# en la que está el archivo de python, además lo devuelve en formato 64 bytes
def getBytes64FromWav(wavName):
    # Obtener la ruta del directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Conseguimos el path junto con el nombre de donde sacaremos el WAV
    WAVE_ORIGINAL_FILENAME = wavName
    originalVersion_path = os.path.join(script_dir, WAVE_ORIGINAL_FILENAME)

    # Leemos los bytes del archivo WAV original
    # Abrir el archivo WAV en modo binario
    with open(originalVersion_path, 'rb') as f:
        # Leer todos los bytes del archivo
        wav_bytes = f.read()
    
    print(wav_bytes[:44])
    print(type(wav_bytes))

    wav_bytes64 = base64.b64encode(wav_bytes) 

    return wav_bytes64

#Funciona
def sendBytesFromLoadedWav(wavName):
    wav_bytes64 = getBytes64FromWav(wavName)
    # Se ejecuta el resultado final enviándolo y analizando el audio
    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_bytes(wav_bytes64)
            pprint.pprint(result)

    asyncio.run(main())
    return "Funcionaaa"

#Mirar porque son lo mismo
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

    return "FuncionaaaaaVersiónCopia"

async def sendBytesDirectlyAsync(bytesFromWav):
    print(bytesFromWav[:44])
    bytesFromWav_copy = base64.b64encode(bytesFromWav) 
    # Se ejecuta el resultado final enviándolo y analizando el audio
    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_bytes(bytesFromWav_copy)
            pprint.pprint(result)
            return result

    return await main()


# copyWavVersion()

# Obtener la ruta del directorio del script
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Conseguimos el path junto con el nombre de donde sacaremos el WAV
# WAVE_ORIGINAL_FILENAME = "Original.wav"
# originalVersion_path = os.path.join(script_dir, WAVE_ORIGINAL_FILENAME)



# originalVersionInstance = wave.open(originalVersion_path, 'rb')

# chunk = originalVersionInstance.readframes(44)


# copyWavFromBytes(chunk)
# sendBytesDirectly(chunk)
# sendBytesFromLoadedWav("Original.wav")
# # Ejemplo de uso:
# Example usage
# Obtener la ruta del directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Conseguimos el path junto con el nombre de donde sacaremos el WAV
file_path = "Original.wav"
WAVE_ORIGINAL_FILENAME = file_path
originalVersion_path = os.path.join(script_dir, WAVE_ORIGINAL_FILENAME)
amplitudes = get_wav_amplitudes(originalVersion_path)
print("Amplitudes:", amplitudes)
# filename = 'ejemplo.wav'
# pitches = get_pitch(filename)
# print("Tonos:", pitches)

def obtener_longitud_de_onda(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        framerate = wav_file.getframerate()
        duration = wav_file.getnframes() / framerate
        wavelength = 1 / framerate
    return wavelength

# Uso de ejemplo
file_path = 'ejemplo.wav'
longitud_de_onda = obtener_longitud_de_onda(originalVersion_path)
print("Longitud de onda:", longitud_de_onda, "segundos")
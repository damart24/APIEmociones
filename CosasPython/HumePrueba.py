import base64
import io
import os
import asyncio
import pprint
import wave
import numpy as np

from hume import HumeStreamClient
from hume.models.config import ProsodyConfig
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import find_peaks

# Copia el wav y envía dicha copia a HumeAI
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

# Crea un wav a partir de los bytes y devuelve nchannels, samwidth, framerate y numFrames
def obtener_caracteristicas_wav_desde_bytes(bytes_wav):
    # Crear un objeto de archivo WAV a partir de los bytes
    wav_file = wave.open(io.BytesIO(bytes_wav))

    # Obtener características del archivo WAV
    n_channels = wav_file.getnchannels()
    sampWidth = wav_file.getsampwidth()
    frameRate = wav_file.getframerate()
    numFrames = wav_file.getnframes()

    # Cerrar el archivo WAV
    wav_file.close()

    return n_channels, sampWidth, frameRate, numFrames

# Copia un wav desde unos bytes dado, y envía dicho wav a HumeAI, como la versión anterior pero 
# desde los bytes en crudo en vez del wav ya formado
def copyWavFromBytes(bytesFromWav, WAVE_COPY_FILENAME):
    # print(bytesFromWav[:44])
    # Obtener características del archivo WAV desde los bytes
    n_channels, sampwidth, framerate, _ = obtener_caracteristicas_wav_desde_bytes(bytesFromWav)

    # Imprimir las características obtenidas
    print("Número de canales:", n_channels)
    print("Ancho de muestra (en bytes):", sampwidth)
    print("Frecuencia de muestreo:", framerate)

    # Obtener la ruta del directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Conseguimos el path junto con el nombre donde se copiará el WAV
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

# Algoritmo de prueba donde cojo las 5 emociones mas predominantes
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

# Algoritmo donde se ordenan las emociones en 5 categorias
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

# Obtengo los bytes de un wav a partir de su nombre, en la ubicación en la que está el archivo de python
def getBytesFromWav(wavName):
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


    return wav_bytes

# Convierte los bytes recibidos en bytes en formato 64 bytes
def convertBytesto64(wav_bytes):
    wav_bytes64 = base64.b64encode(wav_bytes) 
    return wav_bytes64

# Este método envía los bytes pero no directamente, sino que recibe el path de un wav
# a partir de dicho wav se obtienen los bytes y dichos bytes se envían convirtiendolos en 64 por si acaso
def sendBytesFromLoadedWav(wavName):
    wav_bytes = getBytesFromWav(wavName)
    wav_bytes64 = convertBytesto64(wav_bytes)
    # Se ejecuta el resultado final enviándolo y analizando el audio
    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_bytes(wav_bytes64)
            pprint.pprint(result)

    asyncio.run(main())
    return "Funcionaaa"

# Este método envía los bytes directamente recibidos convirtiendolos en 64 por si acaso
def sendBytesDirectly(bytesFromWav):
    print(bytesFromWav[:44])
    bytesFromWav64 = convertBytesto64(bytesFromWav) 
    # Se ejecuta el resultado final enviándolo y analizando el audio
    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_bytes(bytesFromWav64)
            pprint.pprint(result)

    return "FuncionaaaaaVersiónCopia"

# Llamada asíncrona que envía a humeAI los bytes recibidos como parámetros
async def sendBytesDirectlyAsync(bytesFromWav):
    print(bytesFromWav[:44])
    bytesFromWav64 = convertBytesto64(bytesFromWav) 
    # Se ejecuta el resultado final enviándolo y analizando el audio
    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_bytes(bytesFromWav64)
            pprint.pprint(result)
            return result

    return await main()

# Método con el que desde un path de un wav recibido devuelve una longitud de onda de dicho wav
def obtener_longitud_de_onda(file_path):
    velocidad_del_sonido = 343
    with wave.open(file_path, 'rb') as wav_file:
        framerate = wav_file.getframerate()
        periodo = 1 / framerate
        frecuencia = 1 / periodo
        longitud_de_onda = velocidad_del_sonido / frecuencia
    return longitud_de_onda

# Método con el que desde un path de un wav recibido devuelve la amplitud media de dicho wav
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

# Método con el que desde un path de un wav recibido devuelve el pitch de dicho wav
def get_pitch(filename):
    # Leer el archivo WAV
    samplerate, data = wav.read(filename)
    
    # Convertir a mono si es estéreo
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    
    # Calcular la Transformada de Fourier
    fft_data = np.fft.fft(data)
    
    # Obtener las frecuencias correspondientes a la FFT
    freqs = np.fft.fftfreq(len(data), 1/samplerate)
    
    # Encontrar los picos en los datos de la FFT
    peaks, _ = find_peaks(np.abs(fft_data))
    
    # Extraer las frecuencias positivas
    pos_freqs = freqs[peaks]
    
    # Calcular el tono (asumiendo que el primer pico corresponde a la frecuencia fundamental)
    pitch = abs(pos_freqs[0])
    
    return pitch

# Método que divide el audio en fragmentos de 5 segundos como mucho para poderles enviar a HumeAI
# Tiene una limitación la librería por eso se cortan en fragmentos
def dividir_audio(bytesFromWav):
    segmentos = []

    # Agregar los primeros 44 bytes a cada segmento
    header_bytes = bytesFromWav[:44]

    nChannels, sampWidth, framerate, num_frames = obtener_caracteristicas_wav_desde_bytes(bytesFromWav)
    
    duration = num_frames / framerate  # Duración total del audio en segundos
        
    # Calcular el número de segmentos
    #Mirar para parametrizarlo
    num_segmentos = int(duration / 5) + 1
    # Dividir el audio en segmentos de máximo 5 segundos
    inicio_frame = 0
    for i in range(num_segmentos):
        fin_frame = min(inicio_frame + 5 * framerate * nChannels * sampWidth, len(bytesFromWav))
        segmento = header_bytes + bytesFromWav[inicio_frame:fin_frame]
        print(len(bytesFromWav))
        segmentos.append(segmento)
        inicio_frame = fin_frame
        # copyWavFromBytes(segmento, "Holaaa" + str(i) + ".wav")
    return segmentos




###Pruebas todo esto

async def sendBytesDirectlyAsyncPruebas(bytesSegments):
    for segment in bytesSegments:
        print(segment[:44])

    segments64 = []

    for segment in bytesSegments:
        segments64.append(convertBytesto64(segment)) 

    emotionsList = []
    # Se ejecuta el resultado final enviándolo y analizando el audio
    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            for segment in segments64:
                result = await socket.send_bytes(segment)
                emotionsList.append(result)
                pprint.pprint(result)
            
            return emotionsList

    return await main()



script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = "1000Cosas2.wav"
originalVersion_path = os.path.join(script_dir, file_path)
bytesToSend =  getBytesFromWav(originalVersion_path)

# copyWavVersion()

# Obtener la ruta del directorio del script

# copyWavFromBytes(bytesToSend)
# sendBytesDirectly(bytesToSend)
# sendBytesFromLoadedWav("Original.wav")
# amplitudes = get_wav_amplitudes(originalVersion_path)
# print("Amplitudes:", amplitudes)
# longitud_de_onda = obtener_longitud_de_onda(originalVersion_path)
# print("Longitud de onda:", longitud_de_onda, "segundos")
# pitch = get_pitch(originalVersion_path)
# print("Tono:", pitch)



segmentos = dividir_audio(bytesToSend)

asyncio.run(sendBytesDirectlyAsyncPruebas(segmentos))



# def guardar_segmentos(segmentos, output_folder):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     for i, segmento in enumerate(segmentos):
#         output_file = os.path.join(output_folder, f'segmento_{i+1}.wav')
#         with wave.open(output_file, 'wb') as wav_file:
#             wav_file.setnchannels(1)  # Mono
#             wav_file.setsampwidth(2)   # 16 bits por muestra
#             wav_file.setframerate(44100)  # Frecuencia de muestreo (puedes cambiarla según tus necesidades)
#             wav_file.writeframes(segmento)



# guardar_segmentos(segmentos, output_folder)
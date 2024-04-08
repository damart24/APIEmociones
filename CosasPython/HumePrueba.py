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

# Función para ordenar las emociones en cada categoría
def sort_emotions_by_category(emotions_by_category, emotions_dict):
    # Verificar si hay una advertencia de que no se detectó ningún discurso
    if 'prosody' in emotions_dict and 'warning' in emotions_dict['prosody'] and emotions_dict['prosody']['warning'] == 'No speech detected.':
        return {category: 0 for category in emotions_by_category}
    
    emotions_list = emotions_dict['prosody']['predictions'][0]['emotions']
    
    # Inicializar un diccionario para almacenar la suma de puntuaciones por categoría
    summed_emotions = {category: 0 for category in emotions_by_category}  
    
    for emotion in emotions_list:
        for category, category_emotions in emotions_by_category.items():
            if any(substring in emotion['name'] for substring in category_emotions):
                summed_emotions[category] += emotion['score']
    
    return summed_emotions

def algoritmoEmocionesFinal(emotionsList):
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

    emotionsList2 = []
    for emotion in emotionsList:
        sorted_emotions_by_category = sort_emotions_by_category(emotions_by_category, emotion)
        # Añadir la nueva categoría y sus emociones asociadas al diccionario summed_emotions
        nueva_categoria = 'Pitch'
        sorted_emotions_by_category[nueva_categoria] = 0
        emotionsList2.append(sorted_emotions_by_category)
    # Ordenar las emociones por categoría
    

    return emotionsList2

# Convierte los bytes recibidos en bytes en formato 64 bytes
async def convertBytesto64(wav_bytes):
    wav_bytes64 = base64.b64encode(wav_bytes) 
    return wav_bytes64

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

# Método que divide el audio en fragmentos de 5 segundos como mucho para poderles enviar a HumeAI
# Tiene una limitación la librería por eso se cortan en fragmentos
def dividir_audio(bytesFromWav):
    segmentos = []

    # Agregar los primeros 44 bytes a cada segmento
    header_bytes = bytesFromWav[:44]

    nChannels, sampWidth, framerate, num_frames = obtener_caracteristicas_wav_desde_bytes(bytesFromWav)
    
    duration = num_frames / framerate  # Duración total del audio en segundos
        
    time = 5
    # Calcular el número de segmentos
    #Mirar para parametrizarlo
    num_segmentos = int(duration / time) + 1
    # Dividir el audio en segmentos de máximo 5 segundos
    inicio_frame = 0
    for i in range(num_segmentos):
        fin_frame = min(inicio_frame + time * framerate * nChannels * sampWidth, len(bytesFromWav))
        segmento = header_bytes + bytesFromWav[inicio_frame:fin_frame]
        segmentos.append(segmento)
        inicio_frame = fin_frame
        # copyWavFromBytes(segmento, "Holaaa" + str(i) + ".wav")
    return segmentos



###Métodos de conseguir características

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



###Pruebas todo esto

async def sendBytesDirectlyAsyncSegmentado(bytesSegments):
    segments64 = []

    for segment in bytesSegments:
        encoded_segment = base64.b64encode(segment)
        segments64.append(encoded_segment)

    emotionsList = []
    # Se ejecuta el resultado final enviándolo y analizando el audio
    client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
    config = ProsodyConfig()
    async with client.connect([config]) as socket:
        for segmentFinal in segments64:            
            result = await socket.send_bytes(segmentFinal)
            emotionsList.append(result)
        
        return emotionsList




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



# script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = "1000Cosas1.wav"
# originalVersion_path = os.path.join(script_dir, file_path)
# bytesToSend =  getBytesFromWav(originalVersion_path)

# segmentos = dividir_audio(bytesToSend)

# emotions = asyncio.run(sendBytesDirectlyAsyncPruebas(segmentos))
# algoritmoEmocionesFinal(emotions)
import base64
import io
import os
from pprint import pprint
import asyncio
import wave

from hume import HumeBatchClient, HumeStreamClient
from hume.models.config import ProsodyConfig
import numpy as np

def face_test():
    from hume.models.config import FaceConfig
    #Pruebas con py y hume ai con caras
    client = HumeBatchClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
    urls = ["https://iep.utm.edu/wp-content/media/hume-bust.jpg"]
    config = FaceConfig()
    job = client.submit_job(urls, [config])

    status = job.get_status()
    print(f"Job status: {status}")

    details = job.get_details()
    run_time_ms = details.get_run_time_ms()
    print(f"Job ran for {run_time_ms} milliseconds")
    predictions = job.get_predictions()
    pprint(predictions)

def phrase_test():
    from hume.models.config import LanguageConfig
    #Pruebas con py y hume ai con frases
    samples = [
        "I am angry",
        "Estoy enfadado"
        "Mary had a little lamb,",
        "Its fleece was white as snow."
        "Everywhere the child went,"
        "The little lamb was sure to go."
    ]

    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = LanguageConfig()
        async with client.connect([config]) as socket:
            for sample in samples:
                result = await socket.send_text(sample)
                emotions = result["language"]["predictions"][0]["emotions"]
                pprint(emotions)

    asyncio.run(main())

def audioNotRecorded_test():
    #Pruebas con py y hume ai con voz
    # Get the directory containing the Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct relative path to the audio file
    file_path = os.path.join(script_dir, "prueba.ogg")

    # Use the constructed relative path
    print("Current working directory:", file_path)

    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_file(file_path)
            print(result)

    asyncio.run(main())

def audioWithSoundDevice_test():
    #Pruebas con sounddevice
    import sounddevice as sd
    import numpy as np
    import scipy.io.wavfile as wav

    fs=44100
    duration = 5  # seconds
    # Obtener la lista de dispositivos de audio disponibles
    dispositivos = sd.query_devices()

    # Iterar sobre los dispositivos e imprimir información sobre cada uno
    for dispositivo in dispositivos:
        print("Nombre del dispositivo:", dispositivo['name'])
        print("Índice del dispositivo:", dispositivo['index'])
        print("Entrada:", dispositivo['max_input_channels'])
        print("Salida:", dispositivo['max_output_channels'])
        print("Frecuencia de muestreo soportada:", dispositivo['default_samplerate'])
        print()

    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
    print("Recording Audio")
    sd.wait()
    print("Audio recording complete , Play Audio")
    print(myrecording)

    sd.play(myrecording, fs, device=4)
    sd.wait()
    print("Play Audio Complete")

def audioWithPyAudio_test():
    #Pruebas con pyaudio y funcionan!!!!!

    import pyaudio
    import wave

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "Output.wav"


    # Obtener la ruta del directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, WAVE_OUTPUT_FILENAME)
    os.makedirs(script_dir, exist_ok=True)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=2,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_file(output_path)
            pprint(result)

    asyncio.run(main())

def audioRecordedTest():
    import pyaudio
    import wave
    import os
    from pprint import pprint
    import asyncio

    from hume import HumeStreamClient
    from hume.models.config import ProsodyConfig

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 1
    WAVE_OUTPUT_FILENAME = "Output.wav"

    # Obtener la ruta del directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, WAVE_OUTPUT_FILENAME)
    os.makedirs(script_dir, exist_ok=True)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=2,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print(type(data))
    print(type(frames))
    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_bytes(frames)
            pprint(result)

    asyncio.run(main())
    return "hola"

def version_final(path):
    from pprint import pprint
    import asyncio

    from hume import HumeStreamClient
    from hume.models.config import ProsodyConfig

    async def main():
       
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_file(path)
            pprint(result)

    asyncio.run(main())
    return "Siuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"

def hello_world2():
    
    import pyaudio
    import wave
    import os
    from pprint import pprint
    import asyncio

    from hume import HumeStreamClient
    from hume.models.config import ProsodyConfig

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 1
    WAVE_OUTPUT_FILENAME = "Output.wav"


    # Obtener la ruta del directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, WAVE_OUTPUT_FILENAME)
    os.makedirs(script_dir, exist_ok=True)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=2,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print(type(data))
    print(type(frames))
    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_bytes(frames)
            pprint(result)

    asyncio.run(main())
    return "hola"

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

# Convierte los bytes recibidos en bytes en formato 64 bytes
def convertBytesto64(wav_bytes):
    wav_bytes64 = base64.b64encode(wav_bytes) 
    return wav_bytes64

# Función para ordenar las emociones en cada categoría
# Este está también en el otro script pero es para que no falle algoritmoEmociones
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

# Algoritmo donde se ordenan las emociones en 5 categorias
# Version desactualizada
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
# Version final que envía pero solo los bytes de un wav, no segmentados ni de una lista
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
def get_longitud_de_onda(audio_data):
    velocidad_del_sonido = 343

    _, _, framerate, _ = obtener_caracteristicas_wav_desde_bytes(audio_data)
    periodo = 1 / framerate
    frecuencia = 1 / periodo
    longitud_de_onda = velocidad_del_sonido / frecuencia

    return longitud_de_onda

# Método con el que desde un path de un wav recibido devuelve la amplitud media de dicho wav
def get_wav_amplitudes(audio_data):
    # Convert byte data to a numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    # Normalize the audio data to range [-1, 1]
    normalized_audio = audio_array / np.iinfo(audio_array.dtype).max
    # Calculate the average amplitude
    average_amplitude = np.mean(np.abs(normalized_audio))

    return average_amplitude

# Método con el que desde un path de un wav recibido devuelve el pitch de dicho wav
def get_pitchPrueba(bytes_wav_segmentos):
    bytes_wav = bytes_wav_segmentos[0]

    with io.BytesIO(bytes_wav) as f:
        audio_data, framerate = sf.read(f)
    # Convierte los datos de audio a un objeto de sonido de Parselmouth
    sound = parselmouth.Sound(audio_data.T, sampling_frequency=framerate)

    # Extrae el pitch (tono) utilizando el algoritmo de "To Pitch (cc)"
    pitch = sound.to_pitch()
    
    return pitch
import os
from pprint import pprint
import asyncio

from hume import HumeBatchClient, HumeStreamClient
from hume.models.config import ProsodyConfig

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
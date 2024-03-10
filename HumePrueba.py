import os
from pprint import pprint
import asyncio
import wave

from hume import HumeStreamClient
from hume.models.config import ProsodyConfig
import pyaudio

testRandom()




def testRandom():
    
    WAVE_OUTPUT_FILENAME = "OutputHola.wav"
    WAVE_INPUT_FILENAME = "Output.wav"
    # Obtener la ruta del directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, WAVE_OUTPUT_FILENAME)
    input_path = os.path.join(script_dir, WAVE_INPUT_FILENAME)
    print(output_path)
    print(input_path)

    wb = wave.open(input_path, 'rb')

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(wb.getnchannels())
    wf.setsampwidth(wb.getsampwidth())
    wf.setframerate(wb.getframerate())

    print(wb.getframerate())
    cositas = wb.readframes(wb.getframerate())
    print(cositas)
    print(type(cositas))
        
    wf.writeframes(b''.join(cositas))
    wf.close()
    wb.close()


    wf = wave.open(output_path, 'wb')
    #     wf.setframerate(RATE)
    #     wf.writeframes(b''.join(frames))

    async def main():
        client = HumeStreamClient("LIoNt2anG1QMGhnVsNICTIIQqHwotID6hc8C7SFinTGi2ccu")
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_file(output_path + "Hola")
            print(result)

    asyncio.run(main())








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
        




    


   
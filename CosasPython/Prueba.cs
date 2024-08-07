using UnityEngine;
using System.IO;
using UnityEngine.XR;
using UnityEngine.XR.Management;
using System.Collections;
using UnityEngine.Networking;
using System;
using System.Collections.Generic;
using System.Text;

public class Prueba : MonoBehaviour
{
    private List<float> recordedSamples = new List<float>();
    private AudioClip audioClip;
    private bool isRecording = false;
    private string microphoneName;
    private int sampleRate;
    private int lastSamplePos = 0;

    // URL del servidor Flask
    private float currentAmplitude = 0f; // Variable para almacenar la amplitud actual
    private const float amplitudeThreshold = 0.01f; // Umbral para detectar audio
    string url = "http://127.0.0.1:5000";

    private const float continuousSpeechThreshold = 5f; // 5 seconds
    private float continuousSpeechDuration = 0f;

    private bool isMonitoringSilence = false;
    private float silenceDuration = 0f;
    private float silenceThreshold = 2f; // Duration of silence to detect end of speech
    void Start()
    {
        // Asegúrate de que Oculus es el sistema VR activo
        XRGeneralSettings.Instance.Manager.InitializeLoaderSync();
        if (XRGeneralSettings.Instance.Manager.activeLoader == null)
        {
            Debug.LogError("Oculus no está activado");
            return;
        }

        // Obtén el nombre del micrófono integrado de Oculus
        microphoneName = Microphone.devices[0];  // Normalmente el primer dispositivo es el micrófono de Oculus
        sampleRate = AudioSettings.outputSampleRate;

        StartRecording();
    }
    void Update()
    {
        // Verifica si está grabando y calcula la amplitud
        if (isRecording && audioClip != null)
        {
            int currentPosition = Microphone.GetPosition(microphoneName);
            if (currentPosition < lastSamplePos)
            {
                currentPosition += audioClip.samples; // Wrapped around
            }

            if (currentPosition > lastSamplePos)
            {
                float[] samples = new float[currentPosition - lastSamplePos];
                audioClip.GetData(samples, lastSamplePos);
                recordedSamples.AddRange(samples);
                lastSamplePos = currentPosition % audioClip.samples;

                currentAmplitude = CalculateAmplitude(samples);

                if (currentAmplitude > amplitudeThreshold)
                {
                    continuousSpeechDuration += Time.deltaTime;
                    if (continuousSpeechDuration >= continuousSpeechThreshold)
                    {
                        Debug.Log("5 segundos de audio detectados. Enviando audio...");
                        SaveAudioClip();
                        recordedSamples.Clear();
                        continuousSpeechDuration = 0f; // Reset timer
                    }
                    else
                    {
                        Debug.Log("Detectando audio...");
                        isMonitoringSilence = true;
                        silenceDuration = 0f;
                    }
                }
                else if (isMonitoringSilence)
                {
                    silenceDuration += Time.deltaTime;
                    if (silenceDuration >= silenceThreshold)
                    {
                        Debug.Log("Silencio detectado. Guardando audio...");
                        SaveAudioClip();
                        recordedSamples.Clear();
                        isMonitoringSilence = false;
                    }
                }
            }
        }
    }
    void StartRecording()
    {
        recordedSamples.Clear();
        audioClip = Microphone.Start(microphoneName, true, 1, sampleRate); // 1 second buffer, looping
        isRecording = true;
        lastSamplePos = 0;
        Debug.Log("Grabación iniciada...");
    }
    void StopRecording()
    {
        if (isRecording)
        {
            Microphone.End(microphoneName);
            SaveAudioClip();
            isRecording = false;
            Debug.Log("Grabación detenida.");
        }
    }
    void SaveAudioClip()
    {
        DateTimeOffset dto = new DateTimeOffset(DateTime.UtcNow);
        string fileName = dto.ToUnixTimeMilliseconds().ToString() + ".wav";
        string filePath = Path.Combine(Application.streamingAssetsPath, fileName);
        SaveWavFile(recordedSamples.ToArray(), filePath);
        Debug.Log($"Audio guardado en: {filePath}");
    }
    void SaveWavFile(float[] samples, string filePath)
    {
        byte[] wavFile = ConvertToWav(samples, 1, sampleRate); // Assuming mono
        File.WriteAllBytes(filePath, wavFile);
        StartCoroutine(askFlask(filePath));
    }
    byte[] ConvertToWav(float[] samples, int channels, int frequency)
    {
        MemoryStream stream = new MemoryStream();
        BinaryWriter writer = new BinaryWriter(stream);

        int sampleCount = samples.Length;
        int byteRate = frequency * channels * sizeof(short);

        // WAV header
        writer.Write(Encoding.UTF8.GetBytes("RIFF"));
        writer.Write(36 + sampleCount * sizeof(short));
        writer.Write(Encoding.UTF8.GetBytes("WAVE"));
        writer.Write(Encoding.UTF8.GetBytes("fmt "));
        writer.Write(16);
        writer.Write((short)1);
        writer.Write((short)channels);
        writer.Write(frequency);
        writer.Write(byteRate);
        writer.Write((short)(channels * sizeof(short)));
        writer.Write((short)16);
        writer.Write(Encoding.UTF8.GetBytes("data"));
        writer.Write(sampleCount * sizeof(short));

        // Data
        foreach (float sample in samples)
        {
            short intSample = (short)(sample * short.MaxValue);
            writer.Write(intSample);
        }

        writer.Flush();
        return stream.ToArray();
    }
    float CalculateAmplitude(float[] samples)
    {
        // Calcula la amplitud de las muestras de audio
        float sum = 0f;
        for (int i = 0; i < samples.Length; i++)
        {
            sum += Mathf.Abs(samples[i]);
        }
        return sum / samples.Length;
    }
    IEnumerator askFlask(string fileName)
    {
        byte[] wavBytes = File.ReadAllBytes(fileName);

        // Crear un formulario para enviar el archivo WAV
        WWWForm form = new WWWForm();
        form.AddBinaryData("file", wavBytes, fileName, "audio/wav");

        // Enviar la solicitud HTTP POST al servidor Flask
        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            // Esperar la respuesta del servidor
            yield return www.SendWebRequest();

            // Comprobar si hay errores
            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + www.error);
            }
            else
            {
                // Obtener la respuesta del servidor
                string response = www.downloadHandler.text;
                Debug.Log("Respuesta del servidor: " + response);
            }
        }

        // Realizar una solicitud HTTP GET al servidor Flask
        // Al acabar esta llamada se liberaran todos los recursos relacionados con la URL
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            // Adjuntar los bytes del archivo WAV al cuerpo de la solicitud
            www.uploadHandler = new UploadHandlerRaw(wavBytes);

            // Especificar el tipo de contenido del archivo (audio/wav en este caso)
            www.SetRequestHeader("Content-Type", "audio/wav");

            // Enviar la solicitud y esperar la respuesta
            yield return www.SendWebRequest();

            // Comprobar si hay errores
            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + www.error);
            }
            else
            {
                // Obtener la respuesta del servidor
                string response = www.downloadHandler.text;
                Debug.Log("Respuesta del servidor: " + response + " " + response.GetType());
                SaveToCsv(response);
            }
        }
    }

    public void SaveToCsv(string dataString)
    {
        List<Dictionary<string, object>> dataList = ParseDataString(dataString);

        // Verificar si hay datos para guardar
        if (dataList.Count == 0)
        {
            Debug.LogWarning("No hay datos para guardar en el archivo CSV.");
            return;
        }

        // Encontrar la posición del primer carácter de comilla simple después de 'Nombre'
        int startIndex = dataString.IndexOf("\'Nombre\': \'") + "\'Nombre\': \'".Length;

        // Encontrar la posición del último carácter de comilla simple antes de ','
        int endIndex = dataString.IndexOf("\'", startIndex);

        // Extraer el nombre del archivo usando Substring
        string nombreArchivoConWav = dataString.Substring(startIndex, endIndex - startIndex);
        string nombreArchivoSinCsv = nombreArchivoConWav.Replace(".wav", "");
        string nombreArchivoDefinitivo = nombreArchivoSinCsv + ".csv";

        string filePath = Path.Combine(Application.streamingAssetsPath, nombreArchivoDefinitivo);

        // Escribir datos en el archivo CSV
        using (StreamWriter writer = new StreamWriter(filePath))
        {
            // Escribir encabezados
            string headers = string.Join(",", dataList[0].Keys);
            writer.WriteLine(headers);

            // Escribir datos
            foreach (var dict in dataList)
            {
                List<string> values = new List<string>();
                foreach (var entry in dict)
                {
                    values.Add(entry.Value.ToString());
                }
                string line = string.Join(",", values);
                writer.WriteLine(line);
            }
        }

        Debug.Log("Archivo CSV guardado en: " + filePath);
    }

    // Método para parsear el string en una lista de diccionarios
    private List<Dictionary<string, object>> ParseDataString(string dataString)
    {
        List<Dictionary<string, object>> dataList = new List<Dictionary<string, object>>();

        // Eliminar los caracteres innecesarios y dividir la cadena en elementos de diccionario
        string cleanedString = dataString.Replace("\\'", "").Replace("'", ""); // Eliminar barras invertidas y comillas simples
        cleanedString = cleanedString.Replace("<p>", "").Replace("</p>", ""); // Eliminar las etiquetas <p> y </p>
        cleanedString = cleanedString.Replace("[{", "{").Replace("}]", "}"); // Eliminar los corchetes cuadrados al inicio y al final

        // Eliminar cualquier texto innecesario al principio y al final de la cadena
        cleanedString = cleanedString.Trim('{');

        string[] entries = cleanedString.Split(new[] { "}, {" }, System.StringSplitOptions.RemoveEmptyEntries);

        foreach (string entry in entries)
        {
            string[] keyValuePairs = entry.Split(new[] { ',' }, System.StringSplitOptions.RemoveEmptyEntries);
            Dictionary<string, object> dict = new Dictionary<string, object>();
            foreach (string pair in keyValuePairs)
            {
                string[] parts = pair.Split(':');
                if (parts.Length == 2) // Asegurarse de que el par clave-valor esté completo
                {
                    string key = parts[0].Trim(); // Limpiar clave
                    string value = parts[1].Trim(); // Limpiar valor

                    // Eliminar cualquier carácter no deseado al final del valor
                    value = value.TrimEnd('}', ' '); // Eliminar '}' y espacios al final del valor

                    dict.Add(key, value);
                }
            }
            dataList.Add(dict);
        }

        return dataList;
    }
}
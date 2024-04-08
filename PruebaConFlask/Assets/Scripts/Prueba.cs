using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.IO;

public class Prueba : MonoBehaviour
{
    [SerializeField]
    string fileName; // Cambia esto con la ruta correcta de tu archivo WAV
    IEnumerator Start()
    {
        // URL del servidor Flask
        string url = "http://127.0.0.1:5000";

        // Ruta del archivo WAV que quieres enviar
        string filePath = Path.Combine(Application.streamingAssetsPath, fileName);
        // Leer los bytes del archivo WAV

        byte[] wavBytes = File.ReadAllBytes(filePath);


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
                ExcelWriter.Instance.SaveToCsv(response);
            }
        }
    }
}

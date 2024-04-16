using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class ExcelWriter : MonoBehaviour
{
    private static ExcelWriter _instance;
    public static ExcelWriter Instance
    {
        get => _instance;
    }

    private void Awake()
    {
        if (_instance == null)
        {
            _instance = this;
            DontDestroyOnLoad(this);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    // Método para guardar los datos en un archivo CSV
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
        string filePathComplete = filePath.Replace("StreamingAssets", "CSVs");
        // Escribir datos en el archivo CSV
        using (StreamWriter writer = new StreamWriter(filePathComplete))
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

        Debug.Log("Archivo CSV guardado en: " + filePathComplete);
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

#Importamos los módulos necesarios para la ejecución del programa
import http.client
import json

URL = "api.fda.gov"#Dirección de la página
API = "/drug/label.json"#Dirección del API

headers = {'User-Agent': 'http-client'} #El header proporciona información adicional al cliente

conn = http.client.HTTPSConnection(URL)
conn.request("GET",API, None, headers)#Esta el la petición que le hacemos a la página de OpenFda para obtener la información
response = conn.getresponse()
print(response.status, response.reason)#Esto nos proporciona información sobre la conexión a la página
#Cada cláusula if o elif recoge un código de error diferente excepto la última que trate la conexión correcta. La cláusula else recoge la información sobre una conexión errónea no recogida anteriormente.
if response.status >= 500:
      print("Server Error")
elif response.status == 404:
  print("URL not found")

elif response.status == 401:
  print("Authentication Failed")

elif response.status >= 400:
  print("Bad Request")

elif response.status >= 300:
  print("Unexpected redirect.")
elif response.status == 200:#En caso de que la conexión sea correcta realizamos la petición a la página y cerramos la conexión.
    archivo_json = response.read().decode("utf-8")
    conn.close()
else:
  print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))

data = json.loads(archivo_json) #Mediante esta función convertimos el archivo json en un objeto de python.

#Mediante el tratamiento de data como un diccionario imprimimos por pantalla la información requerida.
print("-El número de identificador del medicamento es el siguiente:" + "\n"+"\t"+data['results'][0]['id'])
print("-El propósito del medicamento es el siguiente:" + "\n"+"\t"+ data['results'][0]['purpose'][0])
print("-El fabricante del medicamento es el siguiente:" + "\n"+"\t"+ data['results'][0]['openfda']["manufacturer_name"][0])


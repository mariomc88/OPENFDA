import http.client
import json

URL = "api.fda.gov"
API = "/drug/label.json?limit="#En este caso añadimos ? que determina que le sigue una variable que va a ser limit, que marcará el límite de búsquedas.
numero_medicamentos = "10"#Este valor marcará el límite y puede ser cambiado a el que queramos hasta un máximo de 100.

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection(URL)
conn.request("GET",API+numero_medicamentos, None, headers)
response = conn.getresponse()
print(response.status, response.reason)

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
elif response.status == 200:
    archivo_json = response.read().decode("utf-8")
    conn.close()
else:
  print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))

data = json.loads(archivo_json)
#En este caso para obtener la información iteramos mediante un bucle while iteramos sobre cada elemento diferente.
i = 0
while i < int(numero_medicamentos):
    print("El número de identificador del medicamento", i+1, "es el siguiente:" + "\n"+"\t"+data['results'][i]['id'])
    i += 1

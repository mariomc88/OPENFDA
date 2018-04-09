import http.client
import json
import datetime

URL = "api.fda.gov"
API = "/drug/label.json?search="#En este caso la variable es "search", porque queremos filtrar la información en función de determinados valores.
periodo_tiempo = "[20090601+TO+"+str(datetime.date.today()).replace("-","")+"]"#Queremos filtrar entre los elementos añadidos desde un principio hasta la fecha actual.
parametro_filtro = "active_ingredient"#Este será el parámetro referente a la infomaclión del medicamento por el que queremos filtrar.
valor_parametro = "Acetylsalicylic acid".replace(" ","+")#El valor de dicho parámetro
limite = "100"#En este caso por no marcarnos un límite, este será 0.

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection(URL)
conn.request("GET",API+"effective_time"+":"+periodo_tiempo+"+AND+"+parametro_filtro+":"+valor_parametro+"&"+"limit="+limite, None, headers)
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

numero_resultados = str(data["meta"]["results"]["total"])#De este modo obtenemos el número de medicamentos que coinciden con la búsqueda.

lista_fabricantes = []#En esta lista añadiremos el nombre del fabricante, en caso de tenerlo, de cada uno de los medicamentos.

lista_fabricantes_sin_repetir = []#En esta lista añadiremos los nombres de los fabricantes sin que haya ninguno repetido

i = 0
while i < int(numero_resultados):#Iteramos para todos los medicamentos
    if "manufacturer_name" in data["results"][i]["openfda"]:#En caso de que el parámetro "manufacturer_name" aparezca, añadimos su valor a la primera lista.
        lista_fabricantes.append(data["results"][i]['openfda']["manufacturer_name"][0])
    i += 1
for fabricante in lista_fabricantes:#De este creamos la lista de nombres sin repetir
    if fabricante not in lista_fabricantes_sin_repetir:
        lista_fabricantes_sin_repetir.append(fabricante)
#Por último imprimimos la información requerida en esta práctica
print("Se han encontrado "+ numero_resultados +" medicamentos que coinciden con los parámetros de búsqueda"+"\n"+"El numero de fabricantes que incluyen este principio activo, "+valor_parametro.replace("+"," ")+" es "+str(len(lista_fabricantes_sin_repetir))+":")

for fabricante in lista_fabricantes_sin_repetir:
    print("\t"+"-"+fabricante)



import http.server
import socketserver
import json

# --- Puerto donde lanzar el servidor
PORT = 8004

HTML1 = """
OpenFda Drug Label
"""

#Esta parte ya ha sido explicado en las practicas anteriores
URL = "api.fda.gov"
API = "/drug/label.json?limit="
limit = "100"

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection(URL)
conn.request("GET", API+limit, None, headers)
response = conn.getresponse()
print(response.status, response.reason)

archivo_json = response.read().decode("utf-8")
conn.close()

data = json.loads(archivo_json)
#Creo una variable de tipo string vacía a la que añado la información de vada medicamento.
contenido = ""
#Mediante un bucle while itero .
i = 0
while i < int(limit): #De este modo voy obteniendo información de cada medicamento hasta el último que vine marcado por el valor que le haya dao en un principio a la variable "limit".
    #Dado que entre los diez medicamentos uno de ello no tienen nombre genérico, mediante la sentencia if y else trato dicho caso.
    if "generic_name" in data['results'][i]['openfda']:
        contenido+= """<tr style="font-size:160%;text-align:center">
                      <td><strong>{Numero_medicamento}</strong></td>
                      <td><strong>{Identificador}</strong></td>
                      <td><strong>{Nombre_generico}</strong></td>
                    </tr>""".format(Numero_medicamento =  i+1, Identificador = data['results'][i]['id'], Nombre_generico = data['results'][i]['openfda']['generic_name'][0])
                        #Para el caso de que si tenga nombre genérico introducimos la información de este medicamento en formato tabla de html que introduciremos más tarde en el archivo html.
    else:
        contenido += """<tr style="font-size:160%;text-align:center">
                          <td><strong>{Numero_medicamento}</strong></td>
                          <td><strong>{Identificador}</strong></td>
                          <td><strong>{Nombre_generico}</strong></td>
                        </tr>""".format(Numero_medicamento =  i+1, Identificador = data['results'][i]['id'], Nombre_generico = "None")
                        #Este es el caso en el que no tiene nombre genérico.
    i += 1

#Este es el archivo html, en el he tratado de usar varias posibilidades que este formato tiene, fuente de letra, color de letra, tamaño de letra, subrayado, crear una tabla...
html_file = """
  <!doctype html>
  <html>
  <body style='background-color: #E5E8E8'>
    <h1 style="font-size:300%;text-align:center;font-family:verdana;color:#003366">En esta pagina usted encontrara informacion referente a diez medicamentos de la base de datos de OpendFda</h2>
    <p style="font-size:160%; text-align:center">
        <table border = "1" style = "margin: 0 auto">
        <tr style="background-color: #AED6F1;font-size:160%">

            <th scope="col">Numero del medicamento</th>
            <th scope="col">Numero de identificador</th>
            <th scope="col">Nombre generico</th>
        </tr>
            {contenido}
        </table>
    <br>
        <div style="color:#003366;text-align:center;font-size:160%"> 
            <a href="https://api.fda.gov/drug/label.json?limit={limite}" >"Link con toda la informacion respecto a estos medicamentos"</a>
        </div>
    </p>
    <p1>
    <a href="https://open.fda.gov/">
        <IMG src= "data:image/png;base64,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"alt = "OpenFda logo" width="214" height="50" align="right">
    </a></p1>
  </body>
  </html>
""".format(contenido = contenido,limite=limit)#Mediante la función format introduzco la información antes recogida en la variable contenido dentro de la tabla del archivo html.

#Esta es la parte del servidor que se encarga de enviar la respuesta al cliente.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # -- Envio de la respuesta al cliente

        self.send_response(200)#El número 200 nos indica que la conexión al servidor fue correcta
        self.send_header('Content-type', 'text/html')#Marca el formato de la respuesta
        self.end_headers()


        mensaje = html_file

        self.wfile.write(bytes(mensaje, "utf8"))
        print("Petición atendida!")
        return

#Esta es la parte encargada de generar el servidor en sí.
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler,bind_and_activate=False)
httpd.allow_reuse_address = True
print("Sirviendo en puerto: {}".format(PORT))


try:
    httpd.server_bind()
    httpd.server_activate()
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Servidor detenido")
    httpd.server_close()
#He cambiado partes del código original porque no me permitía reutilizar el mismo puerto. Esto se debía a que el socket aún cerrado seguía esperando respuesta. Desenlazando el socket y enlazandolo posteriormente se soluciona el error.
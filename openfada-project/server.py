#encoding utf-8
import http.server
import http.client
import socketserver
import json
from urllib.parse import urlsplit

import os
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

# -- Puerto donde lanzar el servidor
PORT = 8000
INDEX_FILE = "index.html"
socketserver.TCPServer.allow_reuse_address = True

# -- Parametros de configuracion
REST_SERVER_NAME = "api.fda.gov"  # -- Nombre del servidor REST
REST_RESOURCE_NAME = "/drug/label.json"
headers = {'User-Agent': 'http-client'}


# Clase con nuestro manejador. Es una clase derivada de BaseHTTPRequestHandler
# Esto significa que "hereda" todos los metodos de esta clase. Y los que
# nosotros consideremos los podemos reemplazar por los nuestros
class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def openfda_req(self, limit=1, search_str=""):
        """Realizar una peticion a openFPGA"""

        # Crear la cadena con la peticion
        req_str = "{}?limit={}".format(REST_RESOURCE_NAME, limit)

        # Si hay que hacer busqueda, añadirla a la cadena de peticion
        if search_str != "":
            req_str += "&{}".format(search_str)

        print("Recurso solicitado: {}".format(req_str))

        conn = http.client.HTTPSConnection(REST_SERVER_NAME)

        # Enviar un mensaje de solicitud
        conn.request("GET", req_str, None, headers)

        # Obtener la respuesta del servidor
        r1 = conn.getresponse()

        # r1.status == 404:
        #   print("ERROR. Recurso {} no encontrado".format(REST_RESOURCE_NAME))
        #   exit(1)

        print("  * {} {}".format(r1.status, r1.reason))

        # Leer el contenido en json, y transformarlo en una cadena
        drugs_json = r1.read().decode("utf-8")
        conn.close()

        # ---- Procesar el contenido JSON
        return json.loads(drugs_json)

    def req_index(self,status=200):
        """Devolver el mensaje con la página indice"""

        index = """
                   <html>
                <head>
                    <title>OpenFDA App</title>
                </head>
                <body align=center style='background-color: #5499C7  '>
                    <h1>Bienvenido a la pagina principal de la App </h1>
                    <br>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Lista Medicamentos">
                        </input>
                    </form>
                    <br>
                    <br>
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Buscar Medicamentos">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    <br>
                    <br>
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Lista Empresas">
                        </input>
                    </form>
                    <br>
                    <br>
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Buscador Empresas">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    <br>
                    <br>
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Lista Advertencias">
                        </input>
                    </form>
                    <br>
                    <br>
                    <p> Practica hecha por Javier Alvarez Benito </p>
                    <p> Ingenieria Biomedica - URJC </p>
                </body>
            </html>"""

        return index

    def req_listdrugs(self, limit,status=200):
        """Devolver el mensaje con la peticion del listado de fármacos"""
        # Lanzar la peticion a openFDA
        # Establecer la conexion con el servidor
        drugs = self.openfda_req(limit)

        # -- Ahora drugs es un diccionario que contiene la respuesta recibida
        # -- Necesitamos conocer su estructura para procesarlo correctamente

        # Campo META, que contiene informacion sobre la busqueda
        meta = drugs['meta']

        # Por ejemplo, podemos saber el numero de objetos totales en la base de datos y los devueltos
        # en esta busqueda
        # Objetos totales: meta.results.total
        # Objetos recibidos: meta.results.limit

        total = meta['results']['total']
        limit = meta['results']['limit']

        print("* Objetos recibidos: {} / {}".format(limit, total))

        message = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                   '</head>\n'
                   '<body>\n'
                   '<p>Nombre. Marca. Fabricante. ID. Propósito</p>'
                   '\n'
                   '<ul>\n')

        # Campo RESULTS: contiene los resultados de la busqueda
        # drugs.results[0]
        for drug in drugs['results']:

            # Nombre del componente principal: drugs.openfda.substance_name[0]
            if drug['openfda']:
                nombre = drug['openfda']['substance_name'][0]

                # Marca: drugs.openfda.brand_name[0]
                marca = drug['openfda']['brand_name'][0]

                # Nombre del fabricante: drugs.openfda.manufacturer_name[0]
                fabricante = drug['openfda']['manufacturer_name'][0]
            else:
                nombre = "Desconocido"
                marca = "Desconocido"
                fabricante = "Desconocido"

            # Identificador: drugs.id
            id = drug['id']

            # Proposito: drugs.purpose[0]
            try:
                proposito = drug['purpose'][0]
            except KeyError:
                proposito = "Desconocido"

            message += "<li>{}. {}. {}. {}. {}</li>\n".format(nombre, marca, fabricante, id, proposito)

        # Parte final del html
        message += ('</ul>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')

        return message

    def req_listcompanies(self, limit):

        # Lanzar la peticion a openFDA
        # Establecer la conexion con el servidor
        drugs = self.openfda_req(limit)

        # -- Ahora drugs es un diccionario que contiene la respuesta recibida
        # -- Necesitamos conocer su estructura para procesarlo correctamente

        # Campo META, que contiene informacion sobre la busqueda
        meta = drugs['meta']

        # Por ejemplo, podemos saber el numero de objetos totales en la base de datos y los devueltos
        # en esta busqueda
        # Objetos totales: meta.results.total
        # Objetos recibidos: meta.results.limit

        total = meta['results']['total']
        limit = meta['results']['limit']

        print("* Objetos recibidos: {} / {}".format(limit, total))

        message = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                   '</head>\n'
                   '<body>\n'
                   '<p>Fabricantes</p>'
                   '\n'
                   '<ul>\n')

        # Campo RESULTS: contiene los resultados de la busqueda
        # drugs.results[0]
        for drug in drugs['results']:

            # Nombre del componente principal: drugs.openfda.substance_name[0]
            if drug['openfda']:

                try:
                    message += "<li>{}</li>".format(drug['openfda']['manufacturer_name'][0])
                except KeyError:
                    message += "<li>{}</li>".format("Sin manufacturer_name")
            else:
                message += "<li>{}</li>".format("Sin manufacturer_name")


        # Parte final del html
        message += ('</ul>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')

        print("Aqui llega...")
        return message
    def req_searchcompany(self,limit):

        drugs = self.openfda_req(limit)

        # -- Ahora drugs es un diccionario que contiene la respuesta recibida
        # -- Necesitamos conocer su estructura para procesarlo correctamente

        # Campo META, que contiene informacion sobre la busqueda
        meta = drugs['meta']

        # Por ejemplo, podemos saber el numero de objetos totales en la base de datos y los devueltos
        # en esta busqueda
        # Objetos totales: meta.results.total
        # Objetos recibidos: meta.results.limit

        total = meta['results']['total']
        limit = meta['results']['limit']
        print("* Objetos recibidos: {} / {}".format(limit, total))

        message = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                   '</head>\n'
                   '<body>\n'
                   '<p>Fabricantes</p>'
                   '\n'
                   '<ul>\n')

        for drug in drugs['results']:

            # Nombre del componente principal: drugs.openfda.substance_name[0]
            if drug['openfda']:

                try:
                    message += "<li>{}</li>".format(drug['openfda']['manufacturer_name'][0])
                except KeyError:
                    message += "<li>{}</li>".format("Sin nombre del fabricante")
            else:
                message += "<li>{}</li>".format("Sin nombre del fabricante")


        message += ('</ul>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')

        print("Aqui llega...")
        return message
    def req_searchDrug(self,limit):
        drugs = self.openfda_req(limit)

        # -- Ahora drugs es un diccionario que contiene la respuesta recibida
        # -- Necesitamos conocer su estructura para procesarlo correctamente

        # Campo META, que contiene informacion sobre la busqueda
        meta = drugs['meta']

        # Por ejemplo, podemos saber el numero de objetos totales en la base de datos y los devueltos
        # en esta busqueda
        # Objetos totales: meta.results.total
        # Objetos recibidos: meta.results.limit

        total = meta['results']['total']
        limit = meta['results']['limit']
        print("* Objetos recibidos: {} / {}".format(limit, total))

        message = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                   '</head>\n'
                   '<body>\n'
                   '<p>Fabricantes</p>'
                   '\n'
                   '<ul>\n')

        for drug in drugs['results']:

            # Nombre del componente principal: drugs.openfda.substance_name[0]
            if drug['openfda']:

                try:
                    message += "<li>{}</li>".format(drug['openfda']['generic_name'][0])
                except KeyError:
                    message += "<li>{}</li>".format("Sin nombre genérico")
            else:
                message += "<li>{}</li>".format("Sin nombre del fabricante")

        message += ('</ul>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')

        print("Aqui llega...")
        return message



    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra
    # en self.path

    def req_listwarnings(self,limit):
        drugs = self.openfda_req(limit)

        # -- Ahora drugs es un diccionario que contiene la respuesta recibida
        # -- Necesitamos conocer su estructura para procesarlo correctamente

        # Campo META, que contiene informacion sobre la busqueda
        meta = drugs['meta']

        # Por ejemplo, podemos saber el numero de objetos totales en la base de datos y los devueltos
        # en esta busqueda
        # Objetos totales: meta.results.total
        # Objetos recibidos: meta.results.limit

        total = meta['results']['total']
        limit = meta['results']['limit']
        print("* Objetos recibidos: {} / {}".format(limit, total))

        message = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                   '</head>\n'
                   '<body>\n'
                   '<p>Advertencias</p>'
                   '\n'
                   '<ul>\n')
        for drug in drugs['results']:

            # Nombre del componente principal: drugs.openfda.substance_name[0]
            try:
                message += "<li>{}</li>".format(drug['warnings'][0])
            except KeyError:
                message += "<li>{}</li>".format("Sin advertencias")


        message += ('</ul>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')

        print("Aqui llega...")
        return message

    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra
    # en self.path

    def do_GET(self):

        print("Recurso pedido: {}".format(self.path))

        message = ""  # type: str
        redirect = True
        limit = "10"
        status = 200
        print("Recurso pedido: {}".format(self.path))
        parse = urlsplit(self.path)
        endpoint = parse[2]
        params = parse[3]

        print("Endpoint: {}, params: {}".format(endpoint, params))

        # Obtener los parametros
        if params:
            print(params)
            print("Hay parametros")
            if "&" in params:
                params = params.split("&")
                for term in params:
                    pieza = term.split("=")
                    if pieza[0] == "limit":
                        limit = int(pieza[1])
                        print("Limit: {}".format(limit))
                    else:
                        valor = pieza[1]

            else:
                pieza = params.split("=")
                if pieza[0] == "limit":
                    print("Hay un límite")
                    limit = int(pieza[1])
                    print("Limit: {}".format(limit))
                else:
                    valor = pieza[1]

        else:
            print("SIN PARAMETROS")
        search_str = ""
        if "searchDrug" in endpoint:
            buscador = "generic_name"
            parametro = buscador + ":" + valor
        elif "searchCompany" in endpoint:
            buscador = "manufacturer_name"
            parametro = buscador + ":" + valor

        if "search" in endpoint:
            search_str += "search="
            search_str += parametro
        print(search_str)
        if endpoint == "/searchDrug" or endpoint == "/searchCompany" or endpoint == "/listDrugs" or endpoint == "/listCompanies":
            # Crear la cadena con la peticion
            req_str = "{}?limit={}".format(REST_RESOURCE_NAME, limit)

            # Si hay que hacer busqueda, añadirla a la cadena de peticion
            if search_str != "":
                req_str += "&{}".format(search_str)

            print("Recurso solicitado: {}".format(req_str))

        bucle = True

        # -- Pagina INDICE
        if endpoint == "/":

            message = self.req_index()
            status = 200

        # -- Listado de farmacos
        elif endpoint == "/listDrugs":
            status = 200
            print("Listado de farmacos solicitado: ListDrugs!")
            message = self.req_listdrugs(limit)

        elif endpoint == "/listCompanies":
            status = 200
            print("Listado de empresas")
            message = self.req_listcompanies(limit=10)

        elif endpoint == "/searchCompany":
            status = 200
            print("Listado de farmacos solicitado: ListDrugs!")
            message = self.req_searchcompany(limit)

        elif endpoint == "/searchDrug":
            status = 200
            print("Listado de farmacos solicitado: ListDrugs!")
            message = self.req_searchcompany(limit)

        elif endpoint == "/listWarnings":
            status = 200
            print("Listado de farmacos solicitado: ListDrugs!")
            message = self.req_listwarnings(limit)


        elif endpoint == "/redirect":
            self.send_response(301)
            self.send_header('Location', "http://127.0.0.1:8000")
            self.send_header('Content-type', 'text/html')
            self.end_headers()


        elif endpoint == "/secret":
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Secure Area"')
            self.end_headers()
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())


        if bucle:

            # La primera linea del mensaje de respuesta es el
            # status. Indicamos que OK
            self.send_response(status)

            # En las siguientes lineas de la respuesta colocamos las
            # cabeceras necesarias para que el cliente entienda el
            # contenido que le enviamos (que sera HTML)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Enviar el mensaaje completo
            self.wfile.write(bytes(message, "utf8"))



# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------
# Establecemos como manejador nuestra propia clase
Handler = TestHTTPRequestHandler

# -- Configurar el socket del servidor, para esperar conexiones de clientes
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

# Entrar en el bucle principal
# Las peticiones se atienden desde nuestro manejador
# Cada vez que se ocurra un "GET" se invoca al metodo do_GET de
# nuestro manejador
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")

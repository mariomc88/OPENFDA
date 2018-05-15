#encoding utf-8
import http.server
import http.client
import socketserver
import json
from urllib.parse import urlsplit


# -- Puerto donde lanzar el servidor
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True

# -- Parametros de configuracion
REST_SERVER_NAME = "api.fda.gov"  # -- Nombre del servidor REST
REST_RESOURCE_NAME = "/drug/label.json"
headers = {'User-Agent': 'http-client'}


class OpenFDAClient(http.server.BaseHTTPRequestHandler):
    def get_path(self):
        limite = 10
        print("Recurso pedido: {}".format(self.path))

        message = ""  # type: str
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
                        self.limit = int(pieza[1])
                        print("Limit: {}".format(limite))
                    else:
                        valor = pieza[1]

            else:
                pieza = params.split("=")
                if pieza[0] == "limit":
                    print("Hay un límite")
                    self.limit = int(pieza[1])
                    print("Limit: {}".format(limite))
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
        return endpoint

    def get_json(self):
        """Realizar una peticion a openFPGA"""

        # Crear la cadena con la peticion
        req_str = "{}?limit={}".format(REST_RESOURCE_NAME, self.limit)

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
        json_file = json.loads(drugs_json)
        results = json_file["results"]
        return results

class OpenFDAHTML(OpenFDAClient):
    def index_page(self):
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

    def content(self, lista):
        contenido = """ <html>
                            <head><title>Resultados de su búsqueda</title></head>
                                        <body>
                                            <ul>"""
        for linea in lista:
            contenido += "<li>" + linea +"</li>"
        contenido += """
                                         </ul>
                                        </body>
                                    </html>"""


        return contenido

class OpenFDAParser(OpenFDAHTML):
    def do_GET(self):
        status = 200
        send_html = True
        medicamentos = []
        endpoint = OpenFDAClient.get_path(self)
        results = OpenFDAClient.get_json(self)

        if endpoint == "/":
            html_file = index

        elif endpoint == "/listDrugs":
            for drug in results:

                # Nombre del componente principal: drugs.openfda.substance_name[0]
                try:
                    medicamentos.append(drug['warnings'][0])
                except KeyError:
                    medicamentos.append("Sin advertencias")
            html_file = self.content(medicamentos)

        elif endpoint == "/listCompanies":
            for drug in results:

                # Nombre del componente principal: drugs.openfda.substance_name[0]
                try:
                    contenido.format(drug['warnings'][0])
                except KeyError:
                    contenido.format("Sin advertencias")
            html_file = self.content(medicamentos)
        elif endpoint == "/searchCompany":
            for drug in results:

                # Nombre del componente principal: drugs.openfda.substance_name[0]
                try:
                    contenido.format(drug['warnings'][0])
                except KeyError:
                    message += "<li>{}</li>".format("Sin advertencias")
            html_file = self.content(medicamentos)
        elif endpoint == "/searchDrug":
            for drug in results:

                # Nombre del componente principal: drugs.openfda.substance_name[0]
                try:
                    medicamentos.append(drug['warnings'][0])
                except KeyError:
                    medicamentos.append("Sin advertencias")
            html_file = self.content(medicamentos)
        elif endpoint == "/listWarnings":
            for drug in results:

                # Nombre del componente principal: drugs.openfda.substance_name[0]
                try:
                    medicamentos.append(drug['warnings'][0])
                except KeyError:
                    medicamentos.append("Sin advertencias")
            html_file = self.content(medicamentos)

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
            self.wfile.write(bytes(html_file, "utf8"))
        print("Recurso pedido: {}".format(self.path))





#lógica para obtener los datos de los medicamentos

#Generación del HTML para la visualización de la información


# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------
# Establecemos como manejador nuestra propia clase
Handler = OpenFDAParser

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

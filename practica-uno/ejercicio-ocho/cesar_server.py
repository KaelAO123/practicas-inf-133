from http.server import BaseHTTPRequestHandler, HTTPServer
import json
mensajes = []
class MensajesService:
    @staticmethod
    def encriptar_mensaje(mensaje):
        resultado = ""
        for letra in mensaje:
            if letra.isalpha():
                es_mayuscula = letra.isupper()
                letra = letra.lower()
                posicion = ord(letra) - ord('a')
                nueva_posicion = (posicion + 3) % 26
                nueva_letra = chr(nueva_posicion + ord('a'))
                if es_mayuscula:
                    nueva_letra = nueva_letra.upper()
                resultado += nueva_letra
            else:
                resultado += letra
        return resultado
    @staticmethod
    def crear_mensaje(data):
        data["id"]=len(mensajes)+1
        data["contenido encriptado"]=MensajesService.encriptar_mensaje(data["contenido"])
        mensajes.append(data)
        return data
    @staticmethod
    def buscar_mensaje(id):
        return next((mensaje for mensaje in mensajes if mensaje["id"]==id),None)
    @staticmethod
    def actualizar_mensaje(id,data):
        data["contenido encriptado"]=MensajesService.encriptar_mensaje(data["contenido"])
        mensaje = MensajesService.buscar_mensaje(id)
        if mensaje:
            mensaje.update(data)
            return mensaje
        return None
    @staticmethod
    def eliminar_mensaje(id):
        mensaje = MensajesService.buscar_mensaje(id)
        if mensaje:
            mensajes.remove(mensaje)
            return mensaje
        return None
    
class HTTPResponse:
    @staticmethod
    def handler_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    
    @staticmethod
    def handler_read(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

class MensajeRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path=="/mensajes":
            data = HTTPResponse.handler_read(self)
            mensaje = MensajesService.crear_mensaje(data)
            if mensaje:
                HTTPResponse.handler_response(self,200,mensaje)
            else:
                HTTPResponse.handler_response(self,200,{"Error":"Mensaje no existente"})
        else:
            HTTPResponse.handler_response(self,404,{"Error":"Ruta no existente"})
    def do_GET(self):
        if self.path == "/mensajes":
            HTTPResponse.handler_response(self,200,mensajes)
        elif self.path.startswith("/mensajes/"):
                id = int(self.path.split("/")[-1])
                mensaje = MensajesService.buscar_mensaje(id)
                if mensaje:
                    HTTPResponse.handler_response(self,200,mensaje)
                else:
                    HTTPResponse.handler_response(self,200,{"Error":"Mensaje no existente"})
        else:
            HTTPResponse.handler_response(self,404,{"Error":"Ruta no existente"})
    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            data = HTTPResponse.handler_read(self)
            mensaje = MensajesService.actualizar_mensaje(id,data)
            if mensaje:
                HTTPResponse.handler_response(self,200,mensaje)
            else:
                HTTPResponse.handler_response(self,404,{"Error":"Mensaje no existente"})
        else:
            HTTPResponse.handler_response(self,200,{"Error":"Ruta no existente"})
    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje = MensajesService.eliminar_mensaje(id)
            if mensaje:
                HTTPResponse.handler_response(self,200,mensaje)
            else:
                HTTPResponse.handler_response(self,404,{"Error":"Mensaje no existente"})

def run_server(port=8000):
    try:
        server_address = ("",port)
        httpd = HTTPServer(server_address,MensajeRequestHandler)
        print(f"Iniciando el servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__=="__main__":
    run_server()



from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

zoologico = []

class ZoologicoService:
    @staticmethod
    def buscar_animal(id):
        return next((animal for animal in zoologico if animal["id"]==id),None)
    
    @staticmethod
    def crear_animal(data):
        data["id"]=len(zoologico)+1
        zoologico.append(data)
        return data

    @staticmethod 
    def buscar_animales_especie(especie):
        return [animal for animal in zoologico if animal["especie"] == especie]
    
    @staticmethod
    def buscar_animales_genero(genero):
        return [animal for animal in zoologico if animal["genero"]==genero]
    
    @staticmethod
    def actualiza_animal(id,data):
        animal = ZoologicoService.buscar_animal(id)
        if animal:
            animal.update(data)
            return animal
        return None
    
    @staticmethod
    def eliminar_animal(id):
        animal = ZoologicoService.buscar_animal(id)
        if animal:
            zoologico.remove(animal)
            return animal
        return None

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_read(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/animales":
            data = HTTPResponseHandler.handle_read(self)
            animales = ZoologicoService.crear_animal(data)
            if animales:
                HTTPResponseHandler.handle_response(self,200,animales)
            else:
                HTTPResponseHandler.handle_response(self,404,{"Error":"Animal no encontrado"})

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                
                zoologico_especie = ZoologicoService.buscar_animales_especie(especie)

                if zoologico_especie:
                    HTTPResponseHandler.handle_response(self,200,zoologico_especie)
                else:
                    HTTPResponseHandler.handle_response(self,404,{"Error":"Especie no existente"})
            elif "genero" in query_params:
                genero = query_params["genero"][0]

                zoologico_genero=ZoologicoService.buscar_animales_genero(genero)

                if zoologico_genero:
                    HTTPResponseHandler.handle_response(self,200,zoologico_genero)
                else:
                    HTTPResponseHandler.handle_response(self,404,{"Error":"Genero no existente"})
            else: 
                HTTPResponseHandler.handle_response(self,200,zoologico)
        else:
            HTTPResponseHandler.handle_response(self,200,{"Error":"Ruta no existente"})
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            ci = int(self.path.split("/")[-1])
            data = HTTPResponseHandler.handle_read(self)
            animal_actualizado = ZoologicoService.actualiza_animal(ci,data)
            if animal_actualizado:
                HTTPResponseHandler.handle_response(self,200,animal_actualizado)
            else:
                HTTPResponseHandler.handle_response(self,404,{"Error":"Animal no existente"})
    def do_DELETE(self):
        if self.path.startswith("/"):
            id = int(self.path.split("/")[-1])
            animal_eliminado = ZoologicoService.eliminar_animal(id)
            if animal_eliminado:
                HTTPResponseHandler.handle_response(self,200,animal_eliminado)
            else:
                HTTPResponseHandler.handle_response(self,404,{"Error":"Animal no eliminado"})
            
def run_server(port = 8000):
    try:
        server_address = ("",port)
        httpd = HTTPServer(server_address,RESTRequestHandler)
        print(f"Iniciando servidor en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor")

if __name__ == "__main__":
    run_server()

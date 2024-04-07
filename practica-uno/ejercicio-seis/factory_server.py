from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
zoologico = {}

class Animales:
    def __init__(self,id,nombre,especie,genero,edad,peso):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso
    
class Mamifero(Animales):
    def __init__(self, id, nombre, genero, edad, peso):
        super().__init__(id, nombre, "Mamifero", genero, edad, peso)

class Pez(Animales):
    def __init__(self, id, nombre, genero, edad, peso):
        super().__init__(id, nombre, "Pez", genero, edad, peso)

class Ave(Animales):
    def __init__(self, id, nombre, genero, edad, peso):
        super().__init__(id, nombre, "Ave", genero, edad, peso)

class Reptil(Animales):
    def __init__(self, id, nombre, genero, edad, peso):
        super().__init__(id, nombre, "Reptil", genero, edad, peso)

class Anfibio(Animales):
    def __init__(self, id, nombre, genero, edad, peso):
        super().__init__(id, nombre, "Pez", genero, edad, peso)

class AnimalesFactory:
    @staticmethod
    def crear_animales(id,nombre,especie,genero,edad,peso):
        if especie=="Mamifero":
            return Mamifero(id,nombre,genero,edad,peso)
        elif especie=="Reptil":
            return Reptil(id,nombre,genero,edad,peso)
        elif especie=="Ave":
            return Ave(id,nombre,genero,edad,peso)
        elif especie=="Anfibio":
            return Anfibio(id,nombre,genero,edad,peso)
        elif especie=="Pez":
            return Pez(id,nombre,genero,edad,peso)
        else:
            raise ValueError("Especie no valida")
class HTTPDataHandler:
    @staticmethod
    def handler_respons(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    
    @staticmethod
    def handler_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        data = handler.rfile.read(content_length)
        return json.loads(data.decode("utf-8"))
    
class AnimalesService:
    def __init__(self):
        self.fabrica = AnimalesFactory()
    
    def add_animales(self,data):
        animal_id = len(zoologico)+1
        animal_nombre = data.get("nombre",None)
        animal_genero = data.get("genero",None) 
        animal_edad = data.get("edad",None)
        animal_peso = data.get("peso",None)
        animal_especie = data.get("especie",None)
        
        animal = self.fabrica.crear_animales(animal_id,animal_nombre,animal_especie,animal_genero,animal_edad,animal_peso)
        zoologico[animal_id] = animal
        return animal
    
    def listar_animal(self):
        return {index: animal.__dict__ for index, animal in zoologico.items()}
    
    def buscar_animales_especie(self,especie):
        return {index: animal.__dict__ for index, animal in zoologico.items() if animal.especie==especie}
    
    def buscar_animales_genero(self,genero):
        return {index: animal.__dict__ for index, animal in zoologico.items() if animal.genero==genero}
    
    def actualizar_animal(self, animal_id,data):
        if animal_id in zoologico:
            animal = zoologico[animal_id]
            animal_nombre = data.get("nombre",None)
            animal_genero = data.get("genero",None) 
            animal_edad = data.get("edad",None)
            animal_peso = data.get("peso",None)
            animal_especie = data.get("especie",None)
            if animal_nombre:
                animal.nombre = animal_nombre
            if animal_genero:
                animal.genero = animal_genero
            if animal_edad:
                animal.edad = animal_edad
            if animal_peso:
                animal.peso = animal_peso
            if animal_especie:
                animal.especie = animal_especie
            
            return animal
        else:
            raise None
    
    def eliminar_animal(self, animal_id):
        if animal_id in zoologico:
            del zoologico[animal_id]
            return {"mensaje":"Animal eliminado"}
        else:
            return None

class ZoologicoRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.zoologico = AnimalesService()
        super().__init__(*args,**kwargs)
    
    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handler_reader(self)
            response_data = self.zoologico.add_animales(data)
            HTTPDataHandler.handler_respons(self,201,response_data.__dict__)
        else:
            HTTPDataHandler.handler_respons(self,404,{"mensaje":"Ruta no encontrada"})
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                zoologico_especie = self.zoologico.buscar_animales_especie(especie)
                if zoologico_especie:
                    HTTPDataHandler.handler_respons(self,200,zoologico_especie)
                else:
                    HTTPDataHandler.handler_respons(self,404,{"Error":"Especie no existente"})
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                zoologico_genero = self.zoologico.buscar_animales_genero(genero)
                if zoologico_genero:
                    HTTPDataHandler.handler_respons(self,200,zoologico_genero)
                else:
                    HTTPDataHandler.handler_respons(self,404,{"Error":"Genero no existente"})
            else:
                response_data = self.zoologico.listar_animal()
                HTTPDataHandler.handler_respons(self,404,response_data)
                    
        else:
            HTTPDataHandler.handler_respons(self,404,{"mensaje":"Ruta no encontrada"})
    
    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handler_reader(self)
            response_data = self.zoologico.add_animales(data)
            HTTPDataHandler.handler_respons(self,201,response_data.__dict__)
        else:
            HTTPDataHandler.handler_respons(self,404,{"mensaje":"Ruta no existente"})
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handler_reader(self)
            response_data = self.zoologico.actualizar_animal(animal_id,data)
            if response_data:
                HTTPDataHandler.handler_respons(self,200,response_data.__dict__)
            else:
                HTTPDataHandler.handler_respons(self,404,{"mensaje":"Animal no existente"})
        else:
            HTTPDataHandler.handler_respons(self,404,{"mensaje":"Ruta no existente"})
        
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.zoologico.eliminar_animal(animal_id)
            if response_data:
                HTTPDataHandler.handler_respons(self,200,response_data)
            else:
                HTTPDataHandler.handler_respons(self,404,{"mensaje":"Animal no existente"})

def main(port = 8000):
    try:
        server_address = ("",port)
        httpd = HTTPServer(server_address, ZoologicoRequestHandler)
        print(f"Iniciando servidor en http://localhost:{port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor")
        httpd.socket.close()

if __name__ == "__main__":
    main()



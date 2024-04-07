from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Float, List, Boolean, Schema, Field, Mutation

class Planta(ObjectType):
    id = Int()
    nombre = String()
    edad = Int()
    especie = String()
    altura = Float()
    frutos = Boolean()

class Query(ObjectType):
    plantas = List(Planta)
    especie_de_planta = List(Planta, especie=String())
    fruto_de_planta = List(Planta)

    def resolve_plantas(root, info):
        return plantas
    
    def resolve_fruto_de_planta(root, info):
        planta_con_fruto=[]
        for planta in plantas:
            if planta.frutos:
                planta_con_fruto.append(planta)
        return planta_con_fruto
    
    def resolve_especie_de_planta(root, info, especie):
        planta_especie = []
        for planta in plantas:
            if planta.especie == especie:
                planta_especie.append(planta)
        return planta_especie
    
class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        edad = Int()
        especie = String()
        altura = Float()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, nombre, edad, especie, altura, frutos):
        nueva_planta = Planta(
            id=len(plantas)+1,
            nombre=nombre,
            edad=edad,
            especie=especie,
            altura=altura,
            frutos=frutos
        )
        plantas.append(nueva_planta)
        return CrearPlanta(planta=nueva_planta)
    

class ActualizarPlanta(Mutation):
    class Arguments:
        nombre = String()
        edad = Int()
        especie = String()
        altura = Float()
        frutos = Boolean()
        id = Int()
    planta = Field(Planta)
    def mutate(root, info, nombre, edad, especie, altura, frutos,id):
        for planta in plantas:
            if planta.id == id:
                planta.nombre = nombre
                planta.edad = edad
                planta.altura=altura
                planta.frutos=frutos
                planta.especie=especie
                return ActualizarPlanta(planta=planta)
        return None


class DeletePlanta(Mutation):
    class Arguments:
        id = Int()
    planta = Field(Planta)

    def mutate(root,info,id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None

class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()
    actualizar_planta = ActualizarPlanta.Field()

plantas = [
    Planta(id=1,nombre="Roble",edad = 25,especie="Alguna",altura = 124.43,frutos = False),
    Planta(id=2,nombre="Girasol",edad = 40,especie="No se",altura = 100.12,frutos = True),
    Planta(id=3,nombre="Roble",edad = 25,especie="Quien Sabe",altura = 646.23,frutos = False),
]

schema = Schema(query=Query, mutation=Mutations)


class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
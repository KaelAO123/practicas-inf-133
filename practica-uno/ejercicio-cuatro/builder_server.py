from http.server import BaseHTTPRequestHandler,HTTPServer
import json
from urllib.parse import urlparse, parse_qs

pacientes = {}

class Paciente:
    def __init__(self):
        self.ci = None
        self.nombre = None
        self.apellido=None
        self.edad = None
        self.genero = None
        self.diagnostico = None
        self.doctor = None

class PacienteBuilder:
    def __init__(self) -> None:
        self.paciente = Paciente()

    def set_ci(self,ci):
        self.paciente.ci = ci

    def set_nombre(self,nombre):
        self.paciente.nombre = nombre
        
    def set_apellido(self,apellido):
        self.paciente.apellido = apellido

    def set_edad(self,edad):
        self.paciente.edad = edad

    def set_genero(self,genero):
        self.paciente.genero = genero

    def set_diagnostico(self,diagnostico):
        self.paciente.diagnostico = diagnostico

    def set_doctor(self,doctor):
        self.paciente.doctor = doctor

    def get_paciente(self):
        return self.paciente

class PacientesDatos:
    def __init__(self,builder):
        self.builder = builder
    
    def crear_paciente(self,ci,nombre,apellido,genero,diagnostico,edad,doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_doctor(doctor)
        self.builder.set_diagnostico(diagnostico)
        return self.builder.get_paciente()
        

class PacienteService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.paciente = PacientesDatos(self.builder)
    
    def buscar_paciente(ci):
        return next(
            {index: paciente.__dict__ for index, paciente in pacientes.items() if paciente.id==id}, 
            None,
        )
    
    
    def crear_paciente(self, data):
        ci = data.get("ci",None)
        nombre = data.get("nombre",None)
        apellido = data.get("apellido",None)
        edad = data.get("edad",None)
        genero = data.get("genero",None)
        diagnostico = data.get("diagnostico",None)
        doctor = data.get("doctor",None)

        paciente = self.paciente.crear_paciente(ci,nombre,apellido,genero,diagnostico,edad,doctor)
        
        pacientes[len(pacientes)+1] = paciente
        return paciente
    
    def leer_pacientes(self):
        algo = {index: paciente.__dict__ for index, paciente in pacientes.items()}
        return algo


    def buscar_diagnostico(self,diagnostico):
        paciente = {index: paciente.__dict__ for index, paciente in pacientes.items() if paciente.diagnostico == diagnostico}
        if paciente:
            return paciente
        return None
    
    
    def buscar_doctores(self,doctor):
        paciente = {index: paciente.__dict__ for index, paciente in pacientes.items() if paciente.doctor == doctor}
        if paciente:
            return paciente
        return None
    
    
    def actualizar_data(self,ci,data):
        paciente = PacienteService.buscar_paciente(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        return None
    
    
    def eliminar_paciente(ci):
        paciente = PacienteService.buscar_paciente(ci)
        if paciente:
            pacientes.remove(paciente)
            return paciente
        return None

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
    
class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args,**kwargs):
        self.controller = PacienteService()
        super().__init__(*args,**kwargs)
    
    def do_POST(self):
        if self.path == "/pacientes":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.crear_paciente(data)
            HTTPDataHandler.handle_response(self,200,response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes":
            response_data = self.controller.leer_pacientes()
            HTTPDataHandler.handle_response(self,200,response_data)
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                paciente_diagnostico = self.controller.buscar_diagnostico(diagnostico)
                if paciente_diagnostico:
                    HTTPDataHandler.handle_response(self,200,paciente_diagnostico)
                else:
                    HTTPDataHandler.handle_response(self,404,{"Error":"Diagnostico no existente"})
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                paciente_doctor = self.controller.buscar_doctores(doctor)
                if paciente_doctor:
                    HTTPDataHandler.handle_response(self,200,paciente_doctor)
                else:
                    HTTPDataHandler.handle_response(self,404,{"Error":"Doctor no existente"})
            else:
                paciente_listado = self.controller.leer_pacientes()
                HTTPDataHandler.handle_response(self,200,paciente_listado)
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.buscar_paciente(ci,data)
            if response_data:
                HTTPDataHandler.handle_response(self,200,response_data)
            else:
                 HTTPDataHandler.handle_response(self,404,{"Error":"KLFSALFS no existente"})
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"KLFSALFS no existente"})
        
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.actualizar_data(ci,data)
            if response_data:
                HTTPDataHandler.handle_response(self,200,response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[2])
            paciente_eliminado = self.controller.eliminar_paciente(ci)
            if paciente_eliminado:
                HTTPDataHandler.handle_response(self,200,paciente_eliminado)
            else:
                HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})
        else:
            HTTPDataHandler.handle_response(self,404,{"Error":"Ruta no existente"})

def main(port=8000):
    try:
        server_adress=('',port)
        httpd=HTTPServer(server_adress,PacienteHandler)
        print(f'Iniciando el servidor en el puerto {port}....')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor")
        httpd.socket.close()

if __name__=="__main__":
    main()
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs


pacientes = [
    {
        "ci":123456789,
        "nombre":"Willy",
        "apellido":"Huaranca",
        "edad":24,
        "genero":"Masculino",
        "diagnostico":"Diabetes",
        "doctor":"Pedro Perez"
    }
    
]

# class Pacientes:
#     def __init__(self,nombre,apellido,edad,genero,diagnostico,doctor) -> None:
#         self.nombre = nombre
#         self.apellido = apellido
#         self.edad = edad
#         self.genero = genero
#         self.diagnostico = diagnostico
#         self.doctor = doctor
#         pass

class PacientesService:
    @staticmethod
    def buscar_paciente(ci):
        return next(
            (paciente for paciente in pacientes if paciente["ci"]==ci), 
            None,
        )
    
    @staticmethod
    def crear_paciente(data):
        pacientes.append(data)
        return data
    
    @staticmethod
    def buscar_diagnostico(diagnostico):
        paciente = [paciente for paciente in pacientes if paciente["diagnostico"]==diagnostico]
        if paciente:
            return paciente
        return None
    
    @staticmethod
    def buscar_doctores(doctor):
        paciente = [paciente for paciente in pacientes if paciente["doctor"]==doctor]
        if paciente:
            return paciente
        return None
    
    @staticmethod
    def actualizar_data(ci,data):
        paciente = PacientesService.buscar_paciente(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        return None
    
    @staticmethod
    def eliminar_paciente(ci):
        paciente = PacientesService.buscar_paciente(ci)
        if paciente:
            pacientes.remove(paciente)
            return paciente
        return None

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    
    @staticmethod
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                paciente_diagnostico = PacientesService.buscar_diagnostico(diagnostico)
                if paciente_diagnostico:
                    HTTPResponseHandler.handle_response(self,200,paciente_diagnostico)
                else:
                    HTTPResponseHandler.handle_response(self,204,[])
            elif "doctor" in query_params:
                doctores = query_params["doctor"][0]
                paciente_doctor = PacientesService.buscar_doctores(doctores)
                if paciente_doctor:
                    HTTPResponseHandler.handle_response(self,200,paciente_doctor)
                else:
                    HTTPResponseHandler.handle_response(self,204,[])
            else:
                HTTPResponseHandler.handle_response(self,200,pacientes)
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = PacientesService.buscar_paciente(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self,200,paciente)
            else:
                HTTPResponseHandler.handle_response(self,204,[])
        else:
            HTTPResponseHandler.handle_response(self,204,[])
    def do_POST(self):
        if self.path == "/pacientes":
            data = HTTPResponseHandler.read_data(self)
            pacientes = PacientesService.crear_paciente(data)
            HTTPResponseHandler.handle_response(self,201,pacientes)
        else:
            HTTPResponseHandler.handle_response(self,404,{"Error":"Ruta no existente"})
      
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = HTTPResponseHandler.read_data(self)
            paciente = PacientesService.actualizar_data(ci,data)
            if paciente:
                HTTPResponseHandler.handle_response(self,200,paciente)
            else:
                HTTPResponseHandler.handle_response(self,404,{"Error":"Estuadiante no encontrado"})
    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = PacientesService.eliminar_paciente(ci)
            HTTPResponseHandler.handle_response(self,200,paciente)
        else:
            HTTPResponseHandler.handle_response(self,404,{"Error":"Ruta no exos"})

def run_server(port=8000):
    try:
        server_address = ("",port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando el servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__=="__main__":
    run_server()
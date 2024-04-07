from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler
from zeep import Client

def suma_dos_numeros(numero_1,numero_2):
    suma = numero_1+numero_2
    return suma
def resta_dos_numeros(numero_1,numero_2):
    resta = numero_1-numero_2
    return resta
def multiplicacion_dos_numeros(numero_1,numero_2):
    multiplicacion = numero_1*numero_2
    return multiplicacion
def division_dos_numeros(numero_1,numero_2):
    division = numero_1/numero_2
    return division

url = "http://localhost:8000"
dispatcher = SoapDispatcher(
    "Operaciones-soap-server",
    location = url,
    action = url,
    namespace = url,
    trace = True,
    ns = True,
)
dispatcher.register_function(
    "suma_dos_numeros",
    suma_dos_numeros,
    returns={"suma":str},
    args={
        "numero_1":int,
        "numero_2":int,  
        },
)
dispatcher.register_function(
    "resta_dos_numeros",
    resta_dos_numeros,
    returns={"resta":str},
    args={
        "numero_1":int,
        "numero_2":int,  
        },
)
dispatcher.register_function(
    "multiplicacion_dos_numeros",
    multiplicacion_dos_numeros,
    returns={"multiplicacion":str},
    args={
        "numero_1":int,
        "numero_2":int,  
        },
)
dispatcher.register_function(
    "division_dos_numeros",
    division_dos_numeros,
    returns={"division":str},
    args={
        "numero_1":int,
        "numero_2":int,  
        },
)
def run_server(port=8000):
    server = HTTPServer(("0.0.0.0",port),SOAPHandler)
    server.dispatcher = dispatcher
    print(f"Servidor iniciando en {url}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()

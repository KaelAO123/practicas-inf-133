from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from urllib.parse import urlparse, parse_qs 
partidas = []
class Partida:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def piedra_papel_tijera(self,elemento_jugador,elemento_servidor):
        if elemento_jugador==elemento_servidor:
            return "empate"
        elif ((elemento_servidor=="piedra" and elemento_jugador=="papel") or
              (elemento_servidor=="papel" and elemento_jugador=="tijera") or
              (elemento_servidor=="tijera" and elemento_jugador=="piedra")
              ):
            return "gano"
        else:
            return "perdio"
        
    def es_ganador(self,elemento_jugador):
        elemento_servidor = random.choice(["piedra","papel","tijera"])
        resultado = self.piedra_papel_tijera(elemento_jugador,elemento_servidor)
        partida = {
            "id": len(partidas)+1,
            "elemento": elemento_jugador,
            "elemento_servidor":elemento_servidor,
            "resultado":resultado
        }
        partidas.append(partida)
        return partida
        
class HTTPDataHandler:
    @staticmethod
    def http_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def read_data(handler):
        content_length = int(handler.headers["Content-Length"])
        data = handler.rfile.read(content_length)
        return json.loads(data.decode("utf-8"))
    
class PartidaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path == "/partidas":
            if "elemento" in query_params:
                elemento = query_params["elemento"][0]
                resultado = player.es_ganador(elemento)
                HTTPDataHandler.http_response(self,200,resultado)
            else:
                HTTPDataHandler.http_response(self,201,partidas)
    def do_POST(self):
        if self.path=="/partidas":
            data = HTTPDataHandler.read_data(self)
            elemento = data["elemento"]
            resultado = player.es_ganador(elemento)
            HTTPDataHandler.http_response(self,200,resultado)

def main():
    global player
    player = Partida()

    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PartidaHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()



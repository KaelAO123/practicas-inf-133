import requests
url = "http://localhost:8000/"
ruta_prima = url+"animales"
nuevo_animal1 = {
    "nombre":"Juan",
    "especie":"Mamifero",
    "genero":"Femenino",
    "edad":42,
    "peso":542,
}
nuevo_animal2 = {
    "nombre":"Jfsauan",
    "especie":"Ave",
    "genero":"Masculino",
    "edad":4132,
    "peso":54532,
}
nuevo_animal3 = {
    "nombre":"Juahfdsn",
    "especie":"Mamifero",
    "genero":"Femenino",
    "edad":532,
    "peso":765,
}
requests.request(method="POST",url=ruta_prima,json=nuevo_animal3)
requests.request(method="POST",url=ruta_prima,json=nuevo_animal2)
response = requests.request(method="POST",url=ruta_prima,json=nuevo_animal1)
print(f"Datos metidos: {response.text}")

response = requests.request(method="GET",url=ruta_prima)
print(f"\nDatos listados: {response.text}")

ruta_especie = ruta_prima+"?especie=Mamifero"
response = requests.request(method="GET",url=ruta_especie)
print(f"\nDatos especie: {response.text}")

ruta_genero = ruta_prima+"?genero=Masculino"
response = requests.request(method="GET",url=ruta_genero)
print(f"\nDatos genero: {response.text}")

ruta_put = ruta_prima+"/2"
actualizar_animal = {
    "nombre":"Richar Parker",
    "especie":"Tigre",
    "genero":"Femenino",
    "edad":24,
    "peso":6543,
}
response = requests.request(method="PUT",url=ruta_put, json=actualizar_animal)
print(f"\nDatos actualizados: {response.text}")

response = requests.request(method="GET",url=ruta_prima)
print(f"\nDatos listados: {response.text}")

ruta_eliminado = ruta_prima+"/3"
response = requests.request(method="DELETE",url=ruta_eliminado)
print(f"\nDatos eliminados: {response.text}")

response = requests.request(method="GET",url=ruta_prima)
print(f"\nDatos listados: {response.text}")
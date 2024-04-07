import requests
url = "http://localhost:8000/"
url_principal = url+"mensajes"
mensaje_nuevo1={
    "contenido":"Este es mi cifrado"
}
mensaje_nuevo2={
    "contenido":"Curiosamente me llamo Cae, y este es el cifrado Caesar"
}
requests.request(method="POST",url=url_principal,json=mensaje_nuevo1)
response = requests.request(method="POST",url=url_principal,json=mensaje_nuevo1)
print(f"\n{response.text}")

response = requests.request(method="GET",url=url_principal)
print(f"\n{response.text}")

response = requests.request(method="GET",url=url_principal+"/2")
print(f"\n{response.text}")

mensaje_actualizado1={
    "contenido":"No tengo nada a decir"
}
response = requests.request(method="PUT",url=url_principal+"/2",json=mensaje_actualizado1)
print(f"\n{response.text}")

response = requests.request(method="GET",url=url_principal)
print(f"\n{response.text}")

response = requests.request(method="DELETE",url=url_principal+"/2")
print(f"\n{response.text}")

response = requests.request(method="GET",url=url_principal)
print(f"\n{response.text}")
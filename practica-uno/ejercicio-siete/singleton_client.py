import requests

url = "http://localhost:8000/"

# GET /player
response = requests.request(
    method="POST", url=url + "partidas", json={"elemento": "piedra"}
)
print("\n",response.text)

response = requests.request(method="GET", url=url + "partidas?elemento=tijera")
print("\n",response.text)

response = requests.request(method="GET", url=url + "partidas")
print("\n",response.text)

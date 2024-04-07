from zeep import Client
client = Client("http://localhost:8000")

numero_1 = 10
numero_2 = 5
print(f"dos numeros: {numero_1} y {numero_2}")
print("Suma de dos numeros:",end="\t")
result1 = client.service.suma_dos_numeros(numero_1,numero_2)
print(result1)

print("Resta de dos numeros:",end="\t")
result2 = client.service.resta_dos_numeros(numero_1,numero_2)
print(result2)

print("Multiplicacion de dos numeros:", end="\t")
result3 = client.service.multiplicacion_dos_numeros(numero_1,numero_2)
print(result3)

print("Division de dos numeros:",end="\t")
result4 = client.service.division_dos_numeros(numero_1,numero_2)
print(result4)

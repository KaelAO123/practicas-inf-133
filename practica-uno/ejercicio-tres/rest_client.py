import requests
url = "http://localhost:8000/"
ruta_post = url + "pacientes"
nuevo_paciente1 = {
        "ci":987654321,
        "nombre":"Juan",
        "apellido":"Quispe",
        "edad":34,
        "genero":"Masculino",
        "diagnostico":"Cancer",
        "doctor":"Rodrigo Perez"
}
nuevo_paciente2 = {
        "ci":5025321,
        "nombre":"Maria",
        "apellido":"Ticona",
        "edad":14,
        "genero":"Femenino",
        "diagnostico":"Diabetes",
        "doctor":"Pedro Perez"
}
nuevo_paciente3 = {
        "ci":1234567809,
        "nombre":"Maicol",
        "apellido":"Rodrigues",
        "edad":96,
        "genero":"Masculino",
        "diagnostico":"Diabetes",
        "doctor":"Rodrigo Perez"
}
requests.request(method="POST",url=ruta_post,json=nuevo_paciente1)
requests.request(method="POST",url=ruta_post,json=nuevo_paciente2)
response = requests.request(method="POST",url=ruta_post,json=nuevo_paciente3)
print(f"Datos metidos: {response.text}")

response = requests.request(method="GET",url=url+"pacientes")
print(f"\nDatos dados: {response.text}")

response = requests.request(method="GET",url=url+"pacientes/123456789")
print(f"\nCI del Paciente: {response.text}")

diabetes_response = requests.request(method="GET",url=url+"pacientes?diagnostico=Diabetes")
print(f"\nPacientes con diabetes: {diabetes_response.text}")

doctor_response = requests.request(method="GET",url=url+"pacientes?doctor=Rodrigo Perez")
print(f"\nPacientes con doctor: {doctor_response.text}")

actualizar_paciente = {
    "nombre":"Kael",
    "apellido":"Reyes"
}

actualizar_response = requests.request(method="PUT",url=url+"pacientes/123456789",json= actualizar_paciente)
print(f"\nPacientes actualizados: {actualizar_response.text}")

eliminar_response = requests.request(method="DELETE",url=url+"pacientes/123456789")
print(f"\nPacientee eliminado: {eliminar_response.text}")

listar_response = requests.request(method="GET",url=url+"pacientes")
print(f"\nPacientes listados: {listar_response.text}")

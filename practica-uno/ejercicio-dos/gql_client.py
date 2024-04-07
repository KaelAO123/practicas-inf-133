import requests

url = 'http://localhost:8000/graphql'

query_crear1 = """
    mutation{
            crearPlanta(nombre:"Roble",edad:43,especie:"Alguna",altura:324.53,frutos:true){
                planta{
                    id
                    nombre
                    edad
                    especie
                    altura
                    frutos
            }
        }
    }
"""
response = requests.post(url, json={'query': query_crear1})
print(response.text)


query_lista = """
{
    plantas{
            id
            nombre
            edad
            especie
            altura
            frutos
        }
    }
"""
response = requests.post(url, json={'query': query_lista})
print(response.text)

query_busca_especie = """
{
    especieDePlanta(especie:"No se"){
            id
            nombre
            edad
            especie
            altura
            frutos
    }

}

"""

response = requests.post(url, json={'query': query_busca_especie})
print(response.text)

query_busca_fruto = """
{
    frutoDePlanta{
        id
        nombre
        edad
        especie
        altura
        frutos
    }
}
"""
response = requests.post(url, json={'query': query_busca_fruto})
print(response.text)

query_actualizar = """
    mutation{
            actualizarPlanta(id:3, nombre:"Roble",edad:93,especie:"Ni idea",altura:100,frutos:false){
                planta{
                    id
                    nombre
                    edad
                    especie
                    altura
                    frutos
            }
        }
    }
"""
response = requests.post(url, json={'query': query_actualizar})
print(response.text)

query_eliminar = """
    mutation{
        deletePlanta(id:3){
            planta{
                nombre
                frutos
                especie
                edad
            }
        }
    }
"""
response = requests.post(url, json={'query': query_eliminar})
print(response.text)

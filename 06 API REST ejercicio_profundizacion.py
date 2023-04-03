# # Ejercicios de profundización [Python]
# EL propósito de este ejercicio es que el alumno ponga sus habilidades JSON, matplotlib, bases de datos, 
# request API JSON y Rest API.

# # Enunciado
# El objetivo es realizar un ejercicio muy similar al realizado en el pasado con la API de jsonplaceholder. 
# Deberan consumir toda la información que retorna el request de la API y almacenarla en una db.

# url = https://jsonplaceholder.typicode.com/todos

# Deberá generar una base de datos SQL que posea los siguientes campos:
# - id --> [número] id de la consulta
# - userId --> [número] id del usuario
# - title --> [texto] nombre del título
# - completed --> [bool] completado o no el título

# Archivo usuario.py

# En este archivo se econtrará la definición de su base de datos y todas las funciones para intercatuar con ella. 
# Dentro del archivo se debe incoporar las funciones que se detallan a continuación.\
# __NOTA:__Es recomendable que primero ensayen por separado el archivo usuario.py 
# y verificar que todo funciona antes de comenzar a utilizarlo en Flask.

# ## fill()
# Deben crear una función "fill" que lea los datos provenientes del JSON request y complete la base de datos. 
# Si se fijan los datos que retorna el JSON en el request son exactamente los mismos que se solicitan en el ejercicio, 
# por lo que pueden utilizar los campos como lo leen de la consulta e insertarlos en su DB.


from flask import Flask,jsonify
import usuario
import requests
import matplotlib.pyplot as plt
import numpy as np

def title_completed_count(userId):
# Deben crear una función que lea la DB y cuente (count) cuantos usuarios con "userId" han completado sus títulos. 
# Para esta query deberá tener dos campos condicionales en su "filter" (userId y completed) 
# y utilizar el método count para contar los casos favorables.

    response = requests.get("https://jsonplaceholder.typicode.com/todos")
    datos = response.json()
    libros_completados = {}
    for dato in datos:
            usuarios =dato['userId']
            completos =dato['completed'] 
            if usuarios in libros_completados:
                libros_completados[usuarios] += completos
            else:
                libros_completados[usuarios] = completos 
    x = libros_completados.keys()
    y = libros_completados.values()
    return x,y

# # Esquema del ejercicio
# - Deben crear su archivo de python "app.py" y crear las funciones mencionadas en este documento. 
# Deben crear la sección "if _name_ == "_main_" y ahí lanzar el server Flask
# - Crear la funciones mencionadas para poder invocar a los endpoints que explorarán los datos.
# - Deberán crear y completar la base de datos dentro del método que se invoca la primera vez que lanzamos la aplicación



app = Flask(__name__)

@app.before_first_request()

def before_first_request_func():
    # Borrar y crear la base de datos
    usuario.db.create_all()
    usuario.db.drop_all()
    # Completar la base de datos
    usuario.fill()
    print("Base de datos generada")


# API

## Endpoints
# __[GET] /user/{id}/titles__
# - Esta ruta es la encargada a informar al solicitante cuantos titulos completó el usuario cuyo id 
# es el pasado como parámetro en la URL estática. Deben imprimir en el HTML cuantos títulos completó ese usuario.\
# NOTA: Utilice "title_completed_count" para obtener la información necesaria.
@app.route("/user/<int:id>/titles")

def user_titles(id):
     user = usuario.query.get(id)
     titulos_cuenta = usuario.title_completed_count(id)
     return f"El usuario con ID {id} completó {titulos_cuenta} títulos."
     

# __[GET] /user/graph__
# - Esta ruta es la encargada a informar el reporte y comparativa de cuantos títulos completó cada usuario en un gráfico. 
# Debe obtener la información de todos los usuarios (la cantidad de títulos que completó cada uno) 
# para armar el gráfico que usted crea mejor que resuelve el reporte solicitado.
# NOTA: Pueden recorrer toda la base de datos y contar cuantos títulos completó cada uno.
@app.route("/user/graph")
def grafico_barras():
     
     users = usuario.query.all()
     titulos_cuenta = [user.title_completed_count() for user in users]

     fig, ax = plt.subplots()
     x = np.arange(len(users))
     ax.bar(x, titulos_cuenta)
     ax.set_xticks(x)
     ax.set_xticklabels([str(user.id) for user in users])
     ax.set_xlabel("ID de usuario")
     ax.set_ylabel("Cantidad de títulos completados")
     ax.set_title("Títulos completados por usuario")
    
     return fig.to_html()

@app.route("/user/titles")
def user_titles():
    users = usuario.query.all()
    titles = [{"user_id": user.id, "title_count": user.title_completed_count()} for user in users]
    return jsonify(titles)

# __[GET] /user/titles__
# - Esta ruta es la encargada a informar cuantos títulos completó cada usuario en un JSON (queda a su criterio). 
# Debe recolectar la misma información solicitada en el anterior punto pero cambiar la estrategía de visualización.


if __name__ == '__main__':
    print('Inove@Server start!')

    # Lanzar server
    app.run(host="127.0.0.1", port=5000)

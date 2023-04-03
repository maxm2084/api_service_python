# Deberá generar una base de datos SQL que posea los siguientes campos:
# - id --> [número] id de la consulta
# - userId --> [número] id del usuario
# - title --> [texto] nombre del título
# - completed --> [bool] completado o no el título

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String)
    completed = db.Column(db.Boolean)
    

def fill ():
    response = requests.get("https://jsonplaceholder.typicode.com/todos")
    datos = response.json()

    for dato in datos:
        instancia_base = Usuario(
            userId = dato["userId"],
            title = dato["title"],
            completed = dato["completed"]
        )
        db.session.add(instancia_base)
    
    db.session.commit()


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

    


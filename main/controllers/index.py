# Función para la página de inicio.
from flask import render_template
def index():
    return render_template("index.html")
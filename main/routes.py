from flask import Blueprint
from flask_login import logout_user
from main.controllers import index, register,iniciar_sesion, cerrar_sesion

routes = Blueprint("routes", __name__)

routes.route("/", methods=["GET"])(index)
routes.route("/register", methods=["GET", "POST"])(register)
routes.route("/iniciar_sesion", methods=["GET", "POST"])(iniciar_sesion)
routes.route('/cerrar_sesion')(cerrar_sesion)

# Ruta para evitar el error 404 de favicon.ico
@routes.route('/favicon.ico')
def favicon():
    return "", 204  # Responde sin contenido, para evitar el error 404

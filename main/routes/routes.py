from flask import Blueprint
from main.controllers.controllers import index, register, iniciar_sesion, cerrar_sesion, lista_usuarios, editar_usuario, eliminar_usuario

routes = Blueprint("routes", __name__)

routes.route("/", methods=["GET"])(index)
routes.route("/register", methods=["GET", "POST"])(register)
routes.route("/iniciar_sesion", methods=["GET", "POST"])(iniciar_sesion)
routes.route("/cerrar_sesion")(cerrar_sesion)
routes.route("/usuarios", methods=["GET"])(lista_usuarios)
routes.route("/usuarios/editar/<int:id>", methods=["POST"])(editar_usuario)
routes.route("/usuarios/eliminar/<int:id>", methods=["POST"])(eliminar_usuario)

# Ruta para evitar el error 404 de favicon.ico
@routes.route("/favicon.ico")
def favicon():
    return "", 204  # Responde sin contenido para evitar el error 404


from flask import Blueprint
from controllers.auth import register, login, logout
from controllers.errors import handle_401, handle_404, favicon
from controllers.index import index
from controllers.users import lista_usuarios, editar_usuario, eliminar_usuario, profile

routes = Blueprint("routes", __name__)

# auth
routes.route("/register", methods=["GET", "POST"])(register)
routes.route("/login", methods=["GET", "POST"])(login)
routes.route("/logout")(logout)

# errors
routes.app_errorhandler(401)(handle_401)
routes.app_errorhandler(404)(handle_404)
routes.route("/favicon.ico")(favicon)

# index
routes.route("/", methods=["GET"])(index)

# Users
routes.route("/usuarios", methods=["GET"])(lista_usuarios)
routes.route("/usuarios/editar/<int:id>", methods=["POST"])(editar_usuario)
routes.route("/usuarios/eliminar/<int:id>", methods=["POST"])(eliminar_usuario)
routes.route("/profile", methods=["GET", "POST"])(profile)
from flask import Flask
from config import SECRET_KEY  # Importar la clave secreta
from main.models import db, User  # Importar la base de datos y modelos
from flask_login import LoginManager
import sys
import os


# Agregar la carpeta raíz del proyecto al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config

app = Flask(__name__)  # Primero se crea la app

app.config.from_object(config)  # Cargar la configuración
app.secret_key = SECRET_KEY  # Asignar la clave secreta después



db.init_app(app)  # Inicializar SQLAlchemy

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "routes.iniciar_sesion"  # Redirigir si no ha iniciado sesión
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from main.routes import routes

app.register_blueprint(routes)

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

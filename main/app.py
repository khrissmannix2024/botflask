from flask import Flask
from main.config.config import Config
from main.models.models import db, User  # Importar la base de datos y modelos
from flask_login import LoginManager
from flask_migrate import Migrate  # Agregar Flask-Migrate
import sys
import os

# Agregar la carpeta raíz del proyecto al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main.config import config

app = Flask(__name__)  # Primero se crea la app

app.config.from_object(Config)

db.init_app(app)  # Inicializar SQLAlchemy

# Inicializar Flask-Migrate
migrate = Migrate(app, db)  # 👈 Agregado aquí

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

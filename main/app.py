from flask import Flask
from models.models import db, User  
from flask_login import LoginManager
from flask_migrate import Migrate  
#import sys
#import os

# Agregar la carpeta raíz del proyecto al path
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config

app = Flask(__name__) 

app.config.from_object(Config)

db.init_app(app)  # Inicializar SQLAlchemy

# Inicializar Flask-Migrate
migrate = Migrate(app, db) 

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "routes.iniciar_sesion"  # Redirigir si no ha iniciado sesión
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import routes 

app.register_blueprint(routes)

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

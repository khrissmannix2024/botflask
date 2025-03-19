import sys
import os

# Agregar el directorio raíz al path para evitar errores de importación
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask
from models.models import db, User
from werkzeug.security import generate_password_hash
from config import Config

# Crear la app y el contexto de base de datos
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    # Verificar si el admin ya existe
    admin = User.query.filter_by(username="Rudeus").first()
    
    if admin:
        print("⚠️ El usuario administrador ya existe.")
    else:
        # Crear usuario administrador
        admin = User(
            username="admin",
            email="admin@gmail.com",
            role="admin"  
        )
        admin.set_password("admin1234")  # Cambia la contraseña.

        # Guardar en la base de datos
        db.session.add(admin)
        db.session.commit()

        print("✅ Usuario administrador creado con éxito.")

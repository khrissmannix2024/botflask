from . import db 
from flask_login import UserMixin  # Importa UserMixin
from datetime import datetime
import pytz  # Módulo para manejar zonas horarias
from werkzeug.security import generate_password_hash, check_password_hash

# Definir la zona horaria local (Colombia, UTC-5)
colombia_tz = pytz.timezone('America/Bogota')

def get_local_now():
    return datetime.now(colombia_tz).replace(microsecond=0)
 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)  # Hash de la contraseña
    created_at = db.Column(db.DateTime, default=get_local_now)  # Usa la hora local
    role = db.Column(db.String(20), nullable=False, default="usuario")  # Rol: "admin" o "usuario"
    
    def set_password(self, password):
        """Cifra la contraseña y la almacena como hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña ingresada coincide con el hash almacenado."""
        return check_password_hash(self.password_hash, password)

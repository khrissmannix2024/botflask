import os
import secrets  # Agregar esta importación

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Generar una clave secreta segura
SECRET_KEY = secrets.token_hex(16)


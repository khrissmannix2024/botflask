import os
import secrets

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    if os.environ.get("RENDER"):
        DB_PATH = "/tmp/database.db"  # Ruta válida en Render
    else:
        DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "database.db"))

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(16)
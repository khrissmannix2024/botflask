import os
import sys

# Esto para que funcione flask run en la terminal, ya que con la estructura actual de carpetas no estaba funcionando.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) 

from config import Config

from flask import Flask
from models.models import db, User 
from extensions import migrate, login_manager, socketio
from routes import routes
from controllers.mensajes import register_socket_events

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa las extensiones con la app
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
socketio.init_app(app, cors_allowed_origins="*")  # Permitir CORS para WebSockets

DB_PATH = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
if not os.path.exists(DB_PATH):
    with app.app_context():
        db.create_all()

app.register_blueprint(routes)

register_socket_events(socketio)  

if __name__ == '__main__':
    socketio.run(app, debug=True) 
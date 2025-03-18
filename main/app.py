import os
import sys
from flask import Flask
from flask_migrate import Migrate

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from models.models import db, User 
from extensions.manager_login import login_manager
from extensions.migrate import migrate
from config import Config
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa las extensiones con la app
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

DB_PATH = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
if not os.path.exists(DB_PATH):
    with app.app_context():
        db.create_all()

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from models.models import db, User  
from flask_migrate import Migrate
from extensions.manager_login import login_manager
from extensions.migrate import migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

from routes import routes 

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)

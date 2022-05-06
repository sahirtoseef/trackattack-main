from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'You need to login to view this page!'

from app.users.routes import users
from app.main.routes import main
from app.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(errors)


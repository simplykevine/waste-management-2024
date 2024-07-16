from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Creating an instance of SQLAlchemy
db = SQLAlchemy()
DB_NAME = "database.db"

# Function to create a Flask application
def create_app():
    # Creating an instance of Flask 
    app = Flask(__name__)
    # Setting the secret key for the Flask application
    app.config['SECRET_KEY'] = "helloworld"
    # Setting the SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initializing the SQLAlchemy app
    db.init_app(app)

    # Importing the views and auth modules from the current directory.
    from .views import views
    from .auth import auth
    # Registering the blueprints for views and auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Importing the User, WasteCollection, and RecyclingEffort models
    from .models import User, WasteCollection,RecyclingEffort

    # Create the database tables
    create_database(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()

        print("Created database!")

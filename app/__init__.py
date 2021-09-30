from flask import Blueprint 
from flask_restful import Api
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from jwt_instance import jwt
from config import config_options
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
def create_app(config_name):

    app = Flask(__name__)
    
    # Creating the app configurations
    app.config.from_object(config_options[config_name])
    
    
    # Initializing flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    

    return app
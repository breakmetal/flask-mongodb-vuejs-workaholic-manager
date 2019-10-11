from config import config 
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

#mail = Mail()
mongo = PyMongo()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    mongo.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from app.config import Config
from pymongo import MongoClient
import modelbit
import os

mongo = None
mb = None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize MongoDB
    global mongo
    mongo = MongoClient(app.config['MONGO_URI'])
    
    # Initialize ModelBit
    global mb
    os.environ['MB_WORKSPACE_NAME'] = app.config['MB_WORKSPACE_NAME']
    os.environ['MB_API_KEY'] = app.config['MB_API_KEY']
    mb = modelbit.login(region=app.config['MB_REGION'])
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.prediction import prediction_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(prediction_bp)
    
    @app.route('/')
    def home():
        return "Flask is running!"
    
    return app
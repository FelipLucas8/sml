from flask_cors import CORS
from flask import Flask
from Application import slm

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow cross-origin requests

    app.register_blueprint(slm.main)

    return app
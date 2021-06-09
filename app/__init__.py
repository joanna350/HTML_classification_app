from flask import Flask
import os
import app.config

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', 'app.config.ProductionConfig'))

if app.config.get('DEBUG'):
    from flask_cors import CORS
    cors = CORS(app)

from app import routes
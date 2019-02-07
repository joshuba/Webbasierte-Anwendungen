import os

from flask import Flask, render_template, request, redirect, jsonify
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from api import api
from database import db
from config import config
from flask import session
from models import *

from decimal import Decimal

config.SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}".format(**config.POSTGRES)

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(config)
jwt = JWTManager(app)
db.init_app(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
app.app_context().push()  # TODO bekomme nur so Datenbankzugriff im Code

app.register_blueprint(api, url_prefix='/api')

class DecimalEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            try:
                return (str(o))
            except TypeError:
                pass
        return JSONEncoder.default(self, o)

app.json_encoder = DecimalEncoder

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

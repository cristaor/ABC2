# Autorizador

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_restful import Api

from ABC2.authorizator.vistas.vistas import VistaAuthorizator
from .vistas import *
from .modelos import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ABC2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaAuthorizator, '/authorizator')
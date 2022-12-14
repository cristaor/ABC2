# Autorizador

from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_restful import Api
import os
from vistas import VistaAuthorizator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ABC2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'secret-phrase'

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

app_context = app.app_context()
app_context.push()

#db.init_app(app)
#db.create_all()
cors = CORS(app)
api = Api(app)
api.add_resource(VistaAuthorizator, '/authorizator')

jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
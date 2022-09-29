# Cola de mensajes: Celerys un 
# Broker de mensajes: Redis

#Importamos la función que creamos para crear nuestra aplicación
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import os
from vistas import VistaNotification
from flask_cors import CORS


app = Flask(__name__)  #constructor con el nombre de la aplicación

# BD sin usuario ni contraseña
host = os.getenv('POSTGRES_HOST','localhost')
user = os.getenv('POSTGRES_USER','postgres')
database = os.getenv('POSTGRES_DB','postgres')
port = os.getenv('POSTGRES_PORT',6379)
DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}@{host}:{port}/{database}'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
# Deshabilitar un flag para que SQlAlchemy no genera track de modificaciones
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#JWT
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True


# Importamos la BD
from modelos import db

#app = create_app('default')
#Contexto para flask
app_context = app.app_context()
app_context.push()

#Inicializamos la BD
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaNotification, '/notificacion')

jwt = JWTManager(app)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))



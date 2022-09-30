from flask_restful import Resource
from ..modelos import *

authorizatorlog_schema = AuthorizatorLogSchema()

class VistaAuthorizator(Resource):

    def post(self):

        authorizatorLog = AuthorizatorLog()

        return {"msg": "Autorización recibida exitosamente"}
from urllib import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
from ..modelos import *

authorizator_schema = AuthorizatorSchema()

class VistaAuthorizator(Resource):

    def post(self):

        authorizator = Authorizator()
        access_token = create_access_token(identity=request.json[''])
        db.session.add(authorizator)
        db.session.commit()
        return {"msg": "Autorización recibida exitosamente", "token de acceso": access_token}
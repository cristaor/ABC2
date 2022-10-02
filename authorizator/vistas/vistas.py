from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
from flask import request
#authorizator_schema = AuthorizatorSchema()

class VistaAuthorizator(Resource):

    def post(self):
        #authorizator = Authorizator()
        
        if not request.json.get('password',None):
            return "Invalir user or password", 404
        identity=request.json['user']
        additional_claims = {"scope": "get/health"}
        if identity == "1":
            additional_claims = {"scope": "get/health post/notifications"}
            
        access_token = create_access_token(identity=identity,additional_claims=additional_claims)
        #db.session.add(authorizator)
        #db.session.commit()
        return {"msg": "Autorización recibida exitosamente", "access_token": access_token}
    
    @jwt_required
    def get(self):

        return {"msg": "Token Valido"}
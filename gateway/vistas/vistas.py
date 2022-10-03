from enum import auto
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
import os
from modelos import db, Central, CentralSchema, Cliente, ClienteSchema, Ubicacion, UbicacionSchema, Sensor, SensorSchema, Evento, EventoSchema, ValidatorLog, ValidatorLogSchema
import re
import json
import numbers
import requests
import jwt

central_schema = CentralSchema()
cliente_schema = ClienteSchema()
ubicacion_schema = UbicacionSchema()
sensor_schema = SensorSchema()
evento_schema = EventoSchema()
validator_schema= ValidatorLogSchema()

class AuthorizationException(Exception):
    def __init__(self, *args: object, message: str) -> None:
        super().__init__(message, *args)
        self.message = message

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class VistaCentral(Resource):
    #@jwt_required()
    def post(self):
        nueva_central = Central(nombre=request.json["nombre"], direccion=request.json["direccion"], telefono=request.json["telefono"], regional=request.json["regional"], pais=request.json["pais"], ciudad=request.json["ciudad"])
        #print(json.dumps(request.json))
        db.session.add(nueva_central)
        db.session.commit()
        return central_schema.dump(nueva_central)

    def get(self):
        return ([central_schema.dumps(central) for central in  Central.query.all()])

class VistaClientesCentral(Resource):

    def post(self, id_central):
        central = Central.query.get_or_404(id_central)

        if "id_cliente" in request.json.keys():

            nuevo_cliente = Cliente.query.get(request.json["id_cliente"])
            if nuevo_cliente is not None:
                central.clientes.append(nuevo_cliente)
                db.session.commit()
            else:
                return 'Cliente erróneo',404
        else:
            nuevo_cliente = Cliente(nombre=request.json["nombre"], direccion=request.json["direccion"], telefono=request.json["telefono"], email=request.json["email"], usuario=request.json["usuario"], clave=request.json["clave"],activo=request.json["activo"])
            central.clientes.append(nuevo_cliente)
        db.session.commit()
        return cliente_schema.dump(nuevo_cliente)

    def get(self, id_central):
        central = Central.query.get_or_404(id_central)
        return [cliente_schema.dump(ca) for ca in central.clientes]

class VistaUbicacionesCliente(Resource):
    def post(self, id_cliente):
        cliente = Cliente.query.get_or_404(id_cliente)

        if "id_ubicacion" in request.json.keys():

            nueva_ubicacion = Ubicacion.query.get(request.json["id_ubicacion"])
            if nueva_ubicacion is not None:
                cliente.ubicaciones.append(nueva_ubicacion)
                db.session.commit()
            else:
                return 'Ubicacion errónea',404
        else:
            nueva_ubicacion = Ubicacion (nombre=request.json["nombre"], direccion=request.json["direccion"],  pais=request.json["pais"], ciudad=request.json["ciudad"], descripcion=request.json["descripcion"])

            cliente.ubicaciones.append(nueva_ubicacion)
        db.session.commit()
        return ubicacion_schema.dump(nueva_ubicacion)

    def get(self, id_cliente):
        cliente = Cliente.query.get_or_404(id_cliente)
        return [ubicacion_schema.dump(ca) for ca in cliente.ubicaciones]

class VistaSensoresUbicacion(Resource):
    def post(self, id_ubicacion):
        ubicacion = Ubicacion.query.get_or_404(id_ubicacion)

        if "id_sensor" in request.json.keys():

            nuevo_sensor = Ubicacion.query.get(request.json["id_sensor"])
            if nuevo_sensor is not None:
                ubicacion.sensores.append(nuevo_sensor)
                db.session.commit()
            else:
                return 'Sensor erróneo',404
        else:
            nuevo_sensor = Sensor(serial=request.json["serial"], marca= request.json["marca"], tipo=request.json["tipo"])
            ubicacion.sensores.append(nuevo_sensor)
        db.session.commit()
        return sensor_schema.dump(nuevo_sensor)

    def get(self, id_ubicacion):
        ubicacion = Ubicacion.query.get_or_404(id_ubicacion)
        return [sensor_schema.dump(ca) for ca in ubicacion.sensores]



class VistaEventosSensores(Resource):
    def post(self, id_sensor):
        sensor = Sensor.query.get_or_404(id_sensor)

        if "id_evento" in request.json.keys():

            nuevo_evento = Evento.query.get(request.json["id_evento"])
            if nuevo_evento is not None:
                sensor.eventos.append(nuevo_evento)
                db.session.commit()
            else:
                return 'Evento erróneo',404
        else:
            nuevo_evento = Sensor(serial=request.json["serial"], marca= request.json["marca"], tipo=request.json["tipo"])
            Evento(tipo=request.json["evento"],descripcion=request.json["descripcion"],fecha=request.json["fecha"],estado=request.json["estado"])
            sensor.eventos.append(nuevo_evento)
        db.session.commit()
        return evento_schema.dump(nuevo_evento)

    def get(self, id_sensor):
        sensor = Sensor.query.get_or_404(id_sensor)
        return [evento_schema.dump(ca) for ca in sensor.eventos]

class VistaLogin(Resource):
    def post(self):
        instance1=os.environ.get("AUTHORIZATOR","localhost")
        port=os.environ.get("AUTHORIZATOR_PORT","5000")
        print(request.json)
        response = requests.post(f"http://{instance1}:{port}/authorizator", json={"user":request.json.get("user",""),
                                                                       "password":request.json.get("password","")})
        print(response)
        return response.json(), response.status_code  
        
class VistaNotificacion(Resource):
    def post(self):
        aux_payload= str(json.dumps(request.json))
        validator = ValidatorLog(fecha=request.json["fecha_evento"], uuid=request.json["uuid"],payload=aux_payload)
        #print(json.dumps(request.json))
        db.session.add(validator)
        db.session.commit()
                
        payload2 = {'fecha_evento': request.json["fecha_evento"],
                    'uuid':request.json["uuid"], 
                    'client_id':request.json["cliente"], 
                    'location_id':request.json["direccion"], 
                    'sensor_type':'PANICO', 
                     'event_type':request.json["tipo_evento"]
                    }
        try:
            autorizar(request, scope = "post/notifications")
        except AuthorizationException as e:
            return {"message":e.message}, 400
        
        instance1=os.environ.get("NOTIFICATION","localhost")
        port=os.environ.get("NOTIFICATION_PORT","4500")
        requests.post(f"http://{instance1}:{port}/notificacion", json=payload2)
        return validator_schema.dump(validator)


class VistaHealth(Resource):
    def get(self):
        try:
            autorizar(request, scope = "get/health")
        except AuthorizationException as e:
            return {"message":e.message}, 400
        

        return "ok",200

def autorizar(request, scope:str) -> None:
    
    instance1=os.environ.get("AUTHORIZATOR","localhost")
    port=os.environ.get("AUTHORIZATOR_PORT","4500")
    response = requests.get(f"http://{instance1}:{port}/authorizator", 
                            headers={"Authorization":request.headers["Authorization"]})
    if response.status_code !=200:
        raise AuthorizationException(message="Token inválido")

    #Validate scope
    bearer = request.headers["Authorization"]
    token = bearer.split()[1]  # YourTokenHere
    data = jwt.decode(token, "secret-phrase", algorithms=['HS256'])
    scopes = data["scope"].split()
    if scope not in scopes:
        raise AuthorizationException(message="Error de permisos de usuario sobre la operación solicita")

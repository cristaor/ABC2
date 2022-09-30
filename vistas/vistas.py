from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from modelos import db, Central, CentralSchema, Cliente, ClienteSchema, Ubicacion, UbicacionSchema, Sensor, SensorSchema, Evento, EventoSchema, ValidatorLog, ValidatorLogSchema, RequestLog, RequestLogSchema
import re
import json
import numbers
import requests
from datetime import datetime
from faker import Faker

central_schema = CentralSchema()
cliente_schema = ClienteSchema()
ubicacion_schema = UbicacionSchema()
sensor_schema = SensorSchema()
evento_schema = EventoSchema()
validator_schema= ValidatorLogSchema()
requestLog_schema = RequestLogSchema()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
data_factory = Faker()

def get_now() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S');

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


class VistaNotificacion(Resource):
    def post(self):
        aux_payload= str(json.dumps(request.json))
        validator = ValidatorLog(fecha=request.json["fecha_evento"], uuid=request.json["uuid"],payload=aux_payload)
        #print(json.dumps(request.json))
        db.session.add(validator)
        db.session.commit()
        payload2 = {'fecha_evento': request.json["fecha_evento"], 'uuid': request.json["uuid"], 'payload': aux_payload}
        #r = requests.post('http://localhost:8001/notificacion', json=payload2)
        #r = requests.post('http://localhost:8002/notificacion', json=payload2)
        #r = requests.post('http://localhost:8003/notificacion', json=payload2)
        return validator_schema.dump(validator)

#vista invocada desde el cliente
class VistaRequestLog(Resource):
    def post(self,id_cliente):
        if "uuid" in request.json.keys():
            nuevo_evento = RequestLog.query.filter(RequestLog.uuid==request.json["uuid"]).first()            #print(str(nuevo_evento))
            if nuevo_evento is not None:
                if "token" in request.json.keys():
                    token_aux=request.json["token"]
                    if len(str(token_aux))<20:
                        #intento de intrusion
                        return 'Token Invalido',404
                    else:
                        nueva_peticion = {
                            "uuid": request.json["uuid"],
                            "token": request.json["token"]
                            }
                        headers = {'Content-Type': 'application/json'}
                        endpoint_peticion = "/authorizator/{}/token/{}".format(str(request.json["uuid"])), format(str(request.json["token"]))
                        aux_payload= str(json.dumps(request.json))
                        payload2 = {'fecha_evento': get_now(), 'uuid': request.json["uuid"], 'payload': aux_payload}

                        #paso 6 valida con el autorizador
                        token_response = requests.get('http://localhost:8001'.endpoint_peticion, json=payload2)
                        respuesta_autorizador = json.loads(token_response.get_data())

                        if respuesta_autorizador.code==404:
                            #intento de intrusion
                            nuevo_evento.valid=0
                            return 'Token Invalido/Expirado',404
                        else:
                            #paso 8 envia la peticion de alarma al notificacion processor
                            r = requests.post('http://localhost:8002/notificacion', json=payload2)
            else:
                #intento de intrusion
                return 'UUID erróneo',404
        else:
            if id_cliente:
                nuevo_cliente = Cliente.query.get(request.json["id_cliente"])
                if nuevo_cliente is not None:
                    #paso 1: nueva peticion del cliente al API
                    aux_payload= str(json.dumps(request.json))
                    #genera un id aleatorio para la peticion
                    uuid_aux=data_factory.password(length=40, special_chars=False, upper_case=False)
                    request_log = RequestLog(fecha=get_now(),uuid=uuid_aux,payload=aux_payload,scope= request.json["scope"], cliente=request.json["id_cliente"])
                    db.session.add(request_log)
                    db.session.commit()

                    payload2 = {'fecha_evento': get_now(), 'uuid': uuid_aux, 'payload': aux_payload}
                    #paso2 envia la peticion al autorizador
                    #r = requests.post('http://localhost:8001/authorizator', json=payload2)
                    return requestLog_schema.dump(request_log)



    def get(self,uuid):
        #Paso 3 , el autorizador debe actualizar el campo token, fecha de expiracion y scope de la tabla RequestLog
        #paso 4 el cliente consulta al API por el token
        request_log = RequestLog.query.filter(RequestLog.uuid==uuid).first()
        if request_log is not None:
            return [requestLog_schema.dump(ca) for ca in RequestLog.query.filter(RequestLog.uuid == uuid)]
        else:
            return 'UUID invalido',404

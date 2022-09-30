import os
from http import client
from multiprocessing import Event
from flask import request
from random import randint

from modelos.modelos import Notification, NotificationSchema
from modelos import db
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import datetime
from celery import Celery
import enum
import json


class SensorType(enum.Enum):
    TEMPERATURA = 1
    HUMEDAD = 2
    CONCENTRACION = 3
    INCENDIO = 4
    MOVIMIENTO = 5
    SIGNOS = 6
    PANICO = 7

class EventType(enum.Enum):
    MEDICION = 1
    ADVERTENCIA = 2
    ALARMA = 3

class ReceivedNotificationRequestEvent:
    id: str
    date_event: datetime
    client_id: str
    location_id: str
    sensor_type : SensorType
    event_type: EventType
    instance: str

celery_app = Celery(__name__, broker = 'redis://redis:6379/0')

@celery_app.task(name="registrar_log")
def publish_event(*args):
    pass

notification_schema = NotificationSchema()

class VistaNotification(Resource):

    def post(self):
        notification = Notification(extern_uuid = request.json["uuid"], 
                                    client_id=request.json["client_id"], 
                                    location_id=request.json["location_id"], 
                                    sensor_type=request.json["sensor_type"], 
                                    event_type=request.json["event_type"], 
                                    date_event =request.json["fecha_evento"])
        db.session.add(notification)
        db.session.commit()

        event = build_received_request_event(id = notification.extern_uuid, date_event =  notification.date_event, client_id =  notification.client_id, 
                                location_id = notification.location_id, sensor_type = SensorType[notification.sensor_type], event_type=EventType[notification.event_type])

        # Omitiendo la publicación del evento
        publish_received_request_event_if_neccesary(event = event)
        
        return {"msg": "Notificación recibida exitosamente"}

def should_inject_error()->bool:
    return randint(0, 100) > 98

def build_received_request_event(id: str, date_event: datetime, client_id: str, 
                                location_id: str, sensor_type : SensorType, 
                                event_type: EventType)-> ReceivedNotificationRequestEvent:

    event = ReceivedNotificationRequestEvent()
    event.id = id
    event.date_event = date_event

    if not should_inject_error():
        event.client_id = client_id    
    else:
        print("Alterando el payload para la solicitud {} desde la instancia {}".format(id, os.environ.get('instance')))
        event.client_id = 222

    event.location_id = location_id
    event.sensor_type = sensor_type
    event.event_type = event_type
    event.instance = os.environ.get('instance')

    return event

def publish_received_request_event_if_neccesary(event : ReceivedNotificationRequestEvent)->None:
    
    if not should_inject_error():
        args = ("event", json.dumps(event.__dict__, default=str))
        publish_event.apply_async(args=args, queue= 'queue.notification.requested')
    else:
        print("Omitiendo evento con ID de solicitud {} desde la instancia {}".format(event.id, os.environ.get('instance')))
       

    
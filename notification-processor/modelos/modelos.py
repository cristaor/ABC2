from flask_sqlalchemy import SQLAlchemy
import enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import datetime

db = SQLAlchemy()

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

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    extern_uuid = db.Column(db.String(128)) 
    date_event = db.Column(db.String(200))
    client_id = db.Column(db.String(200))
    location_id = db.Column(db.String(200))
    sensor_type = db.Column(db.String(200))
    event_type = db.Column(db.String(200))

    # Representación del objeto
    def __repr__(self) -> str:
        return "{}-{}-{}-{}-{}-{}-{}".format(self.id, self.extern_uuid, self.date_event, self.client_id, self.location_id, self.sensor_type, self.event_type)

class NotificationSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Notification
         load_instance = True
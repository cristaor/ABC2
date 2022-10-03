from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema
import enum

db = SQLAlchemy()

class Scope(enum.Enum):
    READ = 1
    WRITE = 2

class Payload(db.Model):
    client_id = db.Column(db.String(200))

class Authorizator(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    extern_uuid = db.Column(db.String(128)) 
    date_event = db.Column(db.String(200))
    client_id = db.Column(db.String(200))
    location_id = db.Column(db.String(200))
    access_token = db.Column(db.String(200))
    token_expiration = db.Column(db.String(200))
    sensor_type = db.Column(db.String(200))
    event_type = db.Column(db.String(200))
    fail_type = db.Column(db.String(200))
    scope = db.Column(db.Enum(Scope))

    # Representación del objeto
    def __repr__(self) -> str:
        return "{}-{}-{}-{}-{}-{}-{}".format(self.id, self.extern_uuid, self.date_event, self.client_id, self.location_id, self.sensor_type, self.event_type)


class EnumADiccionario(fields.Field):

    def _serialize(self, valor, attr, obj, **kwargs):
        
        if valor is None:
            return None

        return {"llave":valor.name, "valor":valor.value}


class AuthorizatorSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Authorizator
         load_instance = True
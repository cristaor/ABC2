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

class AuthorizatorLog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    extern_uuid = db.Column(db.String(128)) 
    date_event = db.Column(db.String(200))
    client_id = db.Column(db.String(200))
    location_id = db.Column(db.String(200))
    token = db.Column(db.String(200))
    token_expiration = db.Column(db.String(200))
    sensor_type = db.Column(db.String(200))
    event_type = db.Column(db.String(200))
    fail_type = db.Column(db.String(200))
    scope = db.Column(db.Enum(Scope))

    # Representación del objeto
    def __repr__(self) -> str:
        return "{}-{}-{}-{}-{}-{}-{}".format(self.id, self.extern_uuid, self.date_event, self.client_id, self.location_id, self.sensor_type, self.event_type)

class AuthorizatorLogSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = AuthorizatorLog
         load_instance = True
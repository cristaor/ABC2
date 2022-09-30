from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import enum

db = SQLAlchemy()

class Accion(enum.Enum):
    SMS = 1
    MENSAJE = 2
    LLAMADA = 3
    ALARMA = 4
    EMAIL = 5

class TipoSensor(enum.Enum):
    TEMPERATURA = 1
    HUMEDAD = 2
    CONCENTRACION = 3
    INCENDIO = 4
    MOVIMIENTO = 5
    SIGNOS = 6
    PANICO = 7

class TipoEvento(enum.Enum):
    MEDICION = 1
    ADVERTENCIA = 2
    ALARMA = 3

class Central(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    direccion = db.Column(db.String(128))
    telefono = db.Column(db.String(15))
    regional = db.Column(db.String(50))
    pais = db.Column(db.String(80))
    ciudad = db.Column(db.String(80))
    clientes = db.relationship('Cliente', cascade='all, delete, delete-orphan')
    operadores = db.relationship('Operador', cascade='all, delete, delete-orphan')
    #id_competidor = db.Column(db.Integer, db.ForeignKey('competidor.id'))
    #id_carrera = db.Column(db.Integer, db.ForeignKey('carrera.id'))


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    direccion = db.Column(db.String(128))
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(80))
    usuario = db.Column(db.String(20))
    clave = db.Column(db.String(10))
    activo = db.Column(db.String(1))
    central = db.Column(db.Integer, db.ForeignKey("central.id"))
    ubicaciones = db.relationship('Ubicacion', cascade='all, delete, delete-orphan')
    vinculados = db.relationship('Vinculado', cascade='all, delete, delete-orphan')
    registros = db.relationship('RegistroServicio', cascade='all, delete, delete-orphan')
    #competidores = db.relationship('Competidor', cascade='all, delete, delete-orphan')
    #apuestas = db.relationship('Apuesta', cascade='all, delete, delete-orphan')
    #usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))


class Condicion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_condicion = db.Column(db.Numeric);
    tipo = db.Column(db.String(20))
    criterio = db.Column(db.String(20))
    regla = db.Column(db.Integer, db.ForeignKey('regla.id'))

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum(TipoEvento))
    descripcion = db.Column(db.String(300))
    fecha = db.Column(db.String(20))
    tiempo_respuesta = db.Column(db.String(20))
    estado = db.Column(db.String(20))
    sensor = db.Column(db.Integer, db.ForeignKey('sensor.id'))

class Operador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    usuario = db.Column(db.String(20))
    clave = db.Column(db.String(10))
    central = db.Column(db.Integer, db.ForeignKey("central.id"))
    registros_actividades = db.relationship('RegistroActividad', cascade='all, delete, delete-orphan')

class RegistroActividad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20))
    evento = db.Column(db.String(40))
    operador = db.Column(db.Integer, db.ForeignKey("operador.id"))


class RegistroServicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.String(20))
    fecha_fin = db.Column(db.String(20))
    observacion = db.Column(db.String(300))
    cliente = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    servicio = db.Column(db.Integer, db.ForeignKey("servicio.id"))

class Regla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    descripcion = db.Column(db.String(200))
    accion = db.Column(db.Enum(Accion))
    ubicacion = db.Column(db.Integer, db.ForeignKey("ubicacion.id"))
    condiciones = db.relationship('Condicion', cascade='all, delete, delete-orphan')

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(50))
    marca = db.Column(db.String(50))
    tipo =  db.Column(db.Enum(TipoSensor))
    ubicacion = db.Column(db.Integer, db.ForeignKey("ubicacion.id"))
    eventos = db.relationship('Evento', cascade='all, delete, delete-orphan')

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(200))
    valorUnitario = db.Column(db.String(10))
    registro_servicios = db.relationship('RegistroServicio', cascade='all, delete, delete-orphan')

class Ubicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    direccion = db.Column(db.String(128))
    direccion = db.Column(db.String(128))
    pais = db.Column(db.String(80))
    ciudad = db.Column(db.String(80))
    descripcion = db.Column(db.String(300))
    cliente = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    sensores = db.relationship('Sensor', cascade='all, delete, delete-orphan')

class ValidatorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20))
    uuid = db.Column(db.String(60))
    instancia = db.Column(db.Numeric)
    payload = db.Column(db.String(256))

class Vinculado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    vinculo = db.Column(db.String(20))
    telefono = db.Column(db.String(15))
    cliente = db.Column(db.Integer, db.ForeignKey("cliente.id"))

class EnumADiccionario(fields.Field):
    #metodo de la clase
    def  _serialize(self, valor, attr, obj, **kwargs):
        #no serializa los vacios
        if valor is None:
            return None
        #retorna el nombre del enum y el valor
        return {"llave":valor.name, "valor":valor.value}


class CentralSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Central
        include_relationships = True
        include_fk = True
        load_instance = True


class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        include_relationships = True
        load_instance = True


class CondicionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Condicion
        include_relationships = True
        load_instance = True

    numero_condicion = fields.Number()


class EventoSchema(SQLAlchemyAutoSchema):
    tipo = EnumADiccionario(attribute=('tipo'))
    class Meta:
        model = Evento
        include_relationships = True
        load_instance = True

class OperadorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Operador
        include_relationships = True
        load_instance = True


class RegistroActividadSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RegistroActividad
        include_relationships = True
        load_instance = True

class RegistroServicioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RegistroServicio
        include_relationships = True
        load_instance = True

class ReglaSchema(SQLAlchemyAutoSchema):
    accion = EnumADiccionario(attribute=('accion'))
    class Meta:
        model = Regla
        include_relationships = True
        load_instance = True

class SensorSchema(SQLAlchemyAutoSchema):
    tipo = EnumADiccionario(attribute=('tipo'))
    class Meta:
        model = Sensor
        include_relationships = True
        load_instance = True

class ServicioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Servicio
        include_relationships = True
        load_instance = True

class UbicacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ubicacion
        include_relationships = True
        load_instance = True


class VinculadoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vinculado
        include_relationships = True
        load_instance = True

class ValidatorLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ValidatorLog()
        include_relationships = True
        load_instance = True

    instancia = fields.Number()

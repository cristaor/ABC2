"""
    Componete que envia las notificaciones al API Gateway
"""
import requests
from flask import Flask
import os

from faker import Faker
from faker.generator import random
from datetime import datetime
import time

import uuid


app = Flask(__name__)

app_context = app.app_context()

with app.app_context():
    data_factory = Faker()

    for j in range(10000):

        time.sleep(5)


        for i in range(10):
            fecha_evento2 = data_factory.date_time_between(start_date='-1d', end_date='now')
            fecha_evento = str(fecha_evento2)
            nombre = data_factory.first_name() + " " + data_factory.last_name();
            direccion = data_factory.address()
            telefono = data_factory.random_int(3000000000, 35000000000)
            email=data_factory.ascii_safe_email()
            cod_id= str(uuid.uuid4())
            list1 = ['PANICO']
            list2 = ['SAMSUNG','NOKIA','SONY','HUAWEI','APPLE']

            sensor_tipo2=random.choice(list1)
            serial2=data_factory.bothify(text='????-########')
            marca2=random.choice(list2)

            
            payload = {'fecha_evento': fecha_evento, 'cliente': nombre, 'direccion': direccion, 'telefono': telefono, 'email': email, 'marca': 'PANICO', 'tipo_evento': 'ALARMA', 'uuid': cod_id}
            print(f"sending request {payload}")
            r = requests.post('http://localhost:5000/notificacion', json=payload)




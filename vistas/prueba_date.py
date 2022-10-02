from faker import Faker
from faker.generator import random
from datetime import datetime


fake = Faker()


prueba=fake.date_time_between(start_date='-1d', end_date='now')


print (prueba)

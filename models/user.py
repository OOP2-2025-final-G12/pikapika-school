from peewee import Model, CharField, IntegerField, DateTimeField
from datetime import datetime
from .db import db


class User(Model):
    name = CharField()
    coin = IntegerField(default=0)
    ticket = IntegerField(default=1)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = "users"

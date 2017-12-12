import os
from peewee import Model, CharField, BooleanField, TextField, DateTimeField, PostgresqlDatabase
from playhouse.pool import PooledPostgresqlDatabase
from datetime import datetime

db_name = os.environ.get("DB_NAME")
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")


class DBSingleton:
    db = None

    @classmethod
    def get_instance(cls):
        if not cls.db:
            cls.db = PooledPostgresqlDatabase(db_name, **{'user': db_user, 'host': db_host, 'password': db_password})
        return cls.db


class SignUp(Model):
    class Meta:
        database = DBSingleton.get_instance()

    first_name = TextField(100)
    last_name = TextField(100)
    email = TextField(100)
    confirm_email = TextField(100)
    password = CharField(20)
    confirm_password = CharField(20)
    timestamp = DateTimeField(default=datetime.now)




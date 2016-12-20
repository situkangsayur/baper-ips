from apps import db
from apps.model.client import Client


class Token(db.Document):
    client = db.DocumentField(Client)
    created_time = db.DateTimeField()
    token = db.StringField()
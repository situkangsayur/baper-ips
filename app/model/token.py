from app import db
from app.model.client import Client


class Token(db.Document):
    client = db.DocumentField(Client)
    created_time = db.DateTimeField()
    token = db.StringField()
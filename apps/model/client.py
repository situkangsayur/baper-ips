from apps import db


class Client(db.Document):
    client_id = db.StringField()
    client_secret = db.StringField()
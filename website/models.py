
from . import db
from sqlalchemy.sql import func
import datetime

class User(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f"{self.name} {self.id} {self.email} {self.password}"


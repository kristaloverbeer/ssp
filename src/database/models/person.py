from sqlalchemy import Integer, String, Boolean

from src.database.models import db


class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String)
    address = db.Column(String)
    has_driving_license = db.Column(Boolean, default=False)

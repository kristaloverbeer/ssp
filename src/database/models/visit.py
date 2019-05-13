from sqlalchemy import Integer, String

from src.database.models import db


class Visit(db.Model):
    __tablename__ = 'visit'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    type = db.Column(String) # TODO: Should be enum
    # TODO: foreign key to hotel
    # TODO: foreign key to person

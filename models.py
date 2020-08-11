from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()

class User(db.Model):
    """ User Model"""

    __tablename__ = "users"
    password = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    admin = db.Column(db.Boolean(), nullable=False)
    rooms = db.Column(postgresql.ARRAY(db.Text()))

class Room(db.Model):
    """ Room Model"""

    __tablename__ = "rooms"
    id = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    stations = db.Column(postgresql.ARRAY(db.Text()), nullable=False)

class Station(db.Model):
    """ Station Model"""

    __tablename__ = "stations"
    id = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    sensors = db.Column(postgresql.ARRAY(db.Text()), nullable=False)

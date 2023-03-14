from marshmallow import Schema, fields

from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String)
    favorite_genre = db.Column(db.String)


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()
    favorite_genre = fields.Str()

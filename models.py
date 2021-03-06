'''Models for db'''
import flask_sqlalchemy
from app import db


class Messages(db.Model):
    '''Message Model'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    message = db.Column(db.TEXT)
    time = db.Column(db.String(20))

    def __init__(self, name, message, time):
        '''Init message model'''
        self.name = name
        self.message = message
        self.time = time

    def __repr__(self):
        '''return str of model'''
        return "<Name: {}\nMessage: {}\nTime: {}".format(self.name, self.message, self.time)

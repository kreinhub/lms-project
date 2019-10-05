from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(120))
    email = db.Column(db.String(120))
    role = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(50))
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)
    registered = db.Column(db.DateTime, default=datetime.datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Content(db.Model):
    theme = db.Column(db.String(120), primary_key=True)
    section = db.Column(db.String(50))
    description = db.Column(db.String(120))
    type_ = db.Column(db.String(50))
    url = db.Column(db.String(120))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_date = db.Column(db.DateTime, default=datetime.datetime.now)
    rating = db.Column(db.Integer)


class Progress(db.Model, UserMixin):
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    theme = db.Column(db.Integer, db.ForeignKey('content.theme'))



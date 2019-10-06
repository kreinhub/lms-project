from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), default="student")
    gender = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)
    registered = db.Column(db.DateTime, default=datetime.datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username} {self.email}>'


class Content(db.Model):
    theme = db.Column(db.String(120), primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    type = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(120), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_date = db.Column(db.DateTime, default=datetime.datetime.now)
    rating = db.Column(db.Integer)      # need to specify default arg

    def __repr__(self):
        return f'<Content {self.theme} {self.type_}>'

class Progress(db.Model, UserMixin):
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    theme = db.Column(db.String(120), db.ForeignKey('content.theme')) 

    def __repr__(self):
        return f'<Users progress by {self.theme}>'

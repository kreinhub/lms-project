from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Users(db.Model, UserMixin):           # нехватает поля для лэвэла
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), default="student")
    gender = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    last_login = db.Column(db.DateTime, default=datetime.now())
    registered = db.Column(db.DateTime, default=datetime.now())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username} {self.email}>'


class Content(db.Model):
    content_id = db.Column(db.Integer, primary_key=True)
    theme_name = db.Column(db.String(120), nullable=False)             # название лекции или курса лекций
    section_name = db.Column(db.String(50), nullable=False)              # название большого раздела
    description = db.Column(db.String(120), nullable=True)
    type = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(120), unique=True, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now())     # как часто обновляется лекция
    modified_date = db.Column(db.DateTime, default=datetime.now())   # используем как иентификатор раздела (section)
    rating = db.Column(db.Integer, default=0)      # need to specify default arg    (в процентах так как проще)

    def __repr__(self):
        return f'<Content {self.theme_name} {self.type}>'

class Progress(db.Model, UserMixin):            # общий прогресс
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    theme = db.Column(db.String(120), db.ForeignKey('content.theme_name'))
    section = db.Column(db.String(120), db.ForeignKey('content.section_name'))


    def __repr__(self):
        return f'<Users progress by {self.theme}>'

class Structure:
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'))
    theme = db.Column(db.String(120), db.ForeignKey('content.theme_name'))
    section = db.Column(db.String(59), db.ForeignKey('content.section_name'))


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    text = db.Column(db.Text)
    published = db.Column(db.DateTime, nullable=False)
    img_url = db.Column(db.String)
    source = db.Column(db.String, nullable=False)

# class Таблица структура контента
# id единица контента
# id единица сабтемы
# id единица раздела

# class таблица прогресс по секции (не надо)
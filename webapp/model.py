from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, not_
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Users(db.Model, UserMixin):           
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
    id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String(120), nullable=False)             # название урока в меню
    description = db.Column(db.String(120), nullable=False)             # описание лекции перед видео
    section_name = db.Column(db.String(50), nullable=False)              # название большого раздела
    url_description = db.Column(db.String(120), nullable=True)         # для заголовков внутри описания
    type = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(120), unique=True, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now())     # как часто обновляется лекция
    modified_date = db.Column(db.DateTime, default=datetime.now())   # используем как иентификатор раздела (section)
    rating = db.Column(db.Integer, default=0)      # need to specify default arg    (в процентах так как проще)
    slug = db.Column(db.String(200))

    @classmethod
    def common_menu(cls):
        return cls.query.with_entities(Content.lesson_name, Content.slug).filter(
                and_(Content.slug != "", Content.slug != "learn-python")
            ).filter(
                (or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))
            ).distinct()

    @classmethod
    def web_menu(cls):
        return cls.query.with_entities(Content.url_description, Content.slug).filter(
                and_(Content.slug != "", Content.slug != "slaydy")
            ).filter(
                or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))
            ).distinct()

    @classmethod
    def ds_menu(cls):
        return cls.query.with_entities(Content.url_description, Content.slug).filter(
                and_(Content.slug != "", Content.slug != "slaydy")
            ).filter(
                or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))
            ).distinct()

    @classmethod
    def bot_menu(cls):
        return cls.query.with_entities(Content.url_description, Content.slug).filter(
                and_(Content.slug != "", Content.slug != "slaydy")
            ).filter(
                or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))
            ).distinct()

    @classmethod
    def add_menu(cls):
        return cls.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()


    def __repr__(self):
        return f'<Content {self.lesson_name} | {self.section_name} | {self.type}>'

class Progress(db.Model, UserMixin):            # общий прогресс
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    theme = db.Column(db.String(120), db.ForeignKey('content.lesson_name'))
    section = db.Column(db.String(120), db.ForeignKey('content.section_name'))


    def __repr__(self):
        return f'<Users progress by {self.theme}>'


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

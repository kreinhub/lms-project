from flask import Flask, render_template

from webapp.model import db, Users, Content, Progress


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


def save_data(db, *args):       # *args are table names. perhaps using *kwargs will be better
    pass


# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
from flask import Flask, render_template

from webapp.model import db, News


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = "Python news"
        news_list = News.query.order_by(News.published.desc()).all()        
        return render_template('index.html', news_title=title, news_list=news_list)

    return app


# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
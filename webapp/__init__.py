from flask import Flask, render_template, url_for, redirect

from webapp.model import db, News, Articles


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        news_list = News.query.order_by(News.published.desc()).all()
        habr_list = Articles.query.filter_by(source="habr").all()
        tproger_list = Articles.query.filter_by(source="tproger").all()       
        return render_template('index.html', news_list=news_list, habr_list=habr_list, tproger_list= tproger_list)

    @app.route('/index.html')
    def redirect_to_index():
        return redirect(url_for('index'))

    return app


# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
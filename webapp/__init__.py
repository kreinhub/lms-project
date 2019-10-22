from flask import Flask, render_template, request

from webapp.model import db, News, Articles, Content


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        # print(request.args["test"])
        news_list = News.query.order_by(News.published.desc()).all()
        habr_list = Articles.query.filter_by(source="habr").all()
        tproger_list = Articles.query.filter_by(source="tproger").all()       
        return render_template('index.html', news_list=news_list, habr_list=habr_list, tproger_list= tproger_list)

    @app.route('/lections/start')
    def start():
        # content_item = Content.query.filter_by(url="text_1").first()
        return render_template('getting-started.html')

    
    @app.route('/lections/common=1')
    def common_1():
        # content_item = Content.query.filter_by(url="text_1").first()
        return render_template('common_1.html')
    

    return app


# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
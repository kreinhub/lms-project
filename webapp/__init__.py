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

    @app.route('/start')
    def start():
        return render_template('getting-started.html')

    @app.route('/start/faq')
    def start_faq():
        return render_template('start_faq.html')

    @app.route('/start/python')
    def start_py():
        return render_template('start_python.html')

    @app.route('/start/cli')
    def start_cli():
        return render_template('start_cli.html')

    @app.route('/start/last_step')
    def start_last():
        return render_template('start_last_step.html')
    
    @app.route('/lections/common')
    def common_1():
        return render_template('common_1.html')
    

    return app


# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
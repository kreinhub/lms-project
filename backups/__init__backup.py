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

    @app.route('/start/about')
    def start():
        return render_template('start_about.html')

    @app.route('/start/faq')
    def start_faq():
        return render_template('start_faq.html')

    @app.route('/start/python')
    def start_py():
        return render_template('start_python.html')

    @app.route('/start/last_step')
    def start_last():
        return render_template('start_last_step.html')
    
    @app.route('/common/cli')
    def common_cli():
        return render_template('common_cli.html')

    @app.route('/common/pyfiles')
    def common_pyfiles():
        return render_template('common_pyfiles.html')
    
    @app.route('/common/simpletypes')
    def common_simple():
        return render_template('common_simple_types.html')
    
    @app.route('/common/variables')
    def common_vars():
        return render_template('common_variables.html')
    
    @app.route('/common/complextypes')
    def common_complex():
        return render_template('common_complex_types.html')
    
    @app.route('/common/functions')
    def common_funcs():
        return render_template('common_functions.html')
    
    @app.route('/common/github')
    def common_github():
        return render_template('common_github.html')

    @app.route('/common/telegrambot')
    def common_bot():
        return render_template('common_bot.html')

    @app.route('/common/if')
    def common_if():
        return render_template('common_if.html')

    @app.route('/common/cycles')
    def common_cycles():
        return render_template('common_cycles.html')

    @app.route('/common/exceptions')
    def common_try():
        return render_template('common_try.html')

    @app.route('/common/modules')
    def common_modules():
        return render_template('common_modules.html')

    return app


# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
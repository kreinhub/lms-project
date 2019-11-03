#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from webapp.forms import LoginForm, RegistrationForm
from webapp.model import db, News, Articles, Content, Users
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from webapp.config import SECRET_KEY
from sqlalchemy import or_, and_, not_
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/'

    logging.basicConfig(filename='app.log',
                        filemode='w',
                        level=logging.ERROR,
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

    @app.route('/')
    def login():
        form = LoginForm()
        title = 'Login'
        if current_user.is_authenticated:
            logging.error('Вы уже авторизованы')
            flash('Вы уже авторизованы')
            return redirect(url_for('index'))

        return render_template('page-login.html', form=form, title=title)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))

            else:
                logging.error('Неправильное имя пользователя или пароль')
                flash('Неправильное имя пользователя или пароль')
                return redirect(url_for('login'))

    @app.route('/registration')
    def registration():
        if current_user.is_authenticated:
            logging.error('Вы уже авторизованы')
            flash('Вы уже авторизованы')
            return redirect(url_for('index'))

        title = "Регистрация"
        registration_form = RegistrationForm()
        return render_template('page-registration.html', title=title, form=registration_form, active='registration')

    @app.route('/process_registration', methods=['POST'])
    def process_registration():
        form = RegistrationForm()
        if form.validate_on_submit():

            email = form.email.data
            password = form.password_reg.data
            password_confirm = form.password_reg_confirm.data

            if Users.query.filter(Users.email == email).count():
                logging.error('Такой пользователь уже есть')
                flash('Такой пользователь уже есть')
                return redirect(url_for('login'))

            if not password == password_confirm:
                logging.error('Пароли не совпадают')
                flash('Пароли не совпадают. Повторите ввод')
                return redirect(url_for('registration'))

            new_user = Users(email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash('Вы успешно зарегистрировались')
            return redirect(url_for('login'))
        logging.error('Пароль не соответствует требованиям')
        flash('Пароль должен содержать хотя бы одну заглавную букву, хотя бы одну цифру и быть не менее 8 символов')
        return redirect(url_for('registration'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно вышли из системы')
        return redirect(url_for('login'))

    @app.route('/index')
    @login_required
    def index():
        # print(request.args["test"])
        news_list = News.query.order_by(News.published.desc()).all()
        habr_list = Articles.query.filter_by(source="habr").all()
        tproger_list = Articles.query.filter_by(source="tproger").all()

        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()

        return render_template('index.html', news_list=news_list, habr_list=habr_list, tproger_list=tproger_list, common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, add_menu=add_menu)



    @app.route('/start/')
    @login_required
    def start():
        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()
        return render_template('start.html', common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, add_menu=add_menu)

    @app.route('/common/<page_slug>/')
    @login_required
    def common(page_slug):
        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()

        page_content = Content.query.with_entities(Content.description, Content.type, Content.url, Content.lesson_name, Content.url_description).filter(Content.slug != "").filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).filter(Content.slug == page_slug).distinct()

        page = Content.query.with_entities(Content.slug).filter(Content.slug == page_slug).first()
        if not page:
            return 'Not found', 404

        return render_template(f'/common/{page.slug}.html', common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, add_menu=add_menu, page_content=page_content)

    #     slug_list = [content.slug for content in db.session.query(Content).all()]
    #     uniq_slugs = [x for i, x in enumerate(slug_list) if x not in slug_list[:i]]

    @app.route('/web/<page_slug>/')
    @login_required
    def web(page_slug):
        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()
        
        page_content = Content.query.with_entities(Content.description, Content.type, Content.url, Content.lesson_name, Content.url_description).filter(Content.slug != "").filter(Content.slug == page_slug).distinct()

        page = Content.query.with_entities(Content.slug).filter(Content.slug == page_slug).first()        
        if not page:
            return 'Not found', 404

        return render_template(f'/web/{page.slug}.html', common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, page_content=page_content, add_menu=add_menu)

    @app.route('/data-science/<page_slug>/')
    @login_required
    def ds(page_slug):
        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()
        
        page_content = Content.query.with_entities(Content.description, Content.type, Content.url, Content.lesson_name, Content.url_description).filter(Content.slug != "").filter(Content.slug == page_slug).distinct()

        page = Content.query.with_entities(Content.slug).filter(Content.slug == page_slug).first()        
        if not page:
            return 'Not found', 404

        return render_template(f'/ds/{page.slug}.html', common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, page_content=page_content, add_menu=add_menu)

    @app.route('/bot/<page_slug>/')
    @login_required
    def bot(page_slug):
        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()
        
        page_content = Content.query.with_entities(Content.description, Content.type, Content.url, Content.lesson_name, Content.url_description).filter(Content.slug != "").filter(Content.slug == page_slug).distinct()

        page = Content.query.with_entities(Content.slug).filter(Content.slug == page_slug).first()        
        if not page:
            return 'Not found', 404

        return render_template(f'/bot/{page.slug}.html', common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, add_menu=add_menu, page_content=page_content)

    @app.route('/additional/<page_slug>/')
    @login_required
    def add(page_slug):
        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()
        
        page_content = Content.query.with_entities(Content.description, Content.type, Content.url, Content.lesson_name, Content.url_description).filter(Content.slug != "").filter(Content.slug == page_slug).distinct()

        page = Content.query.with_entities(Content.slug).filter(Content.slug == page_slug).first()        
        if not page:
            return 'Not found', 404

        return render_template(f'/add/{page.slug}.html', common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, add_menu=add_menu, page_content=page_content)

    @app.route('/helps/')
    @login_required
    def help():
        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()

        return render_template('page_in_progress.html', common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, add_menu=add_menu)


    return app

# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
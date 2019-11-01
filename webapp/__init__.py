from flask import Flask, render_template, request
from sqlalchemy import or_, and_, not_

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

        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()

        return render_template('index.html', news_list=news_list, habr_list=habr_list, tproger_list=tproger_list, common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, add_menu=add_menu)

    @app.route('/start/')
    def start():
        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()

        return render_template('start.html', common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, add_menu=add_menu)

    @app.route('/common/<page_slug>/')
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
    def help():
        common_menu = Content.query.with_entities(Content.lesson_name, Content.slug).filter(and_(Content.slug != "", Content.slug != "learn-python")).filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        web_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Веб%'), Content.section_name.ilike('%Трек: веб%'))).distinct()
        ds_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Анализ%'), Content.section_name.ilike('%Трек Data%'), Content.section_name.ilike('%Трек: анализ%'))).distinct()
        bot_menu = Content.query.with_entities(Content.url_description, Content.slug).filter(and_(Content.slug != "", Content.slug != "slaydy")).filter(or_(Content.section_name.ilike('%Трек Telegram%'), Content.section_name.ilike('%Трек Боты%'), Content.section_name.ilike('%Трек: боты%'))).distinct()
        add_menu = Content.query.with_entities(Content.description, Content.slug).filter(Content.slug != "").filter(Content.section_name.ilike('%Дополнительно%')).distinct()

        return render_template('page_in_progress.html', common_menu=common_menu, web_menu=web_menu, ds_menu=ds_menu, bot_menu=bot_menu, add_menu=add_menu)

    return app


# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
from flask import Flask, render_template, request
from sqlalchemy import or_

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

        common_menu = Content.query.with_entities(Content.theme_name, Content.slug).filter(Content.slug != "").filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        return render_template('index.html', news_list=news_list, habr_list=habr_list, tproger_list=tproger_list, common_menu=common_menu)

    @app.route('/start/')
    def start():
        # content_list = Content.query.with_entities(Content.description, Content.type, Content.url).filter(Content.slug != "").filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        # for i in content_list:
        #     print(i)
        common_menu = Content.query.with_entities(Content.theme_name, Content.slug).filter(Content.slug != "").filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        return render_template('start.html', common_menu=common_menu)

    @app.route('/common/<page_slug>/')
    def common(page_slug):
        common_menu = Content.query.with_entities(Content.theme_name, Content.slug).filter(Content.slug != "").filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).distinct()
        page = Content.query.with_entities(Content.slug).filter(Content.slug == page_slug).first()
        
        page_content = Content.query.with_entities(Content.description, Content.type, Content.url, Content.theme_name).filter(Content.slug != "").filter((or_(Content.section_name.ilike('%первой%'), Content.section_name.ilike('%2 недели%'), Content.section_name.ilike('%окружение%')))).filter(Content.slug == page_slug).distinct()
        if not page:
            return 'Not found', 404

        return render_template(f'{page.slug}.html', common_menu=common_menu, page_content=page_content)

    #     slug_list = [content.slug for content in db.session.query(Content).all()]
    #     uniq_slugs = [x for i, x in enumerate(slug_list) if x not in slug_list[:i]]
        


    return app


# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
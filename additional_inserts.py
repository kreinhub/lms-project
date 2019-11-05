# -*- coding: utf-8 -*-
from webapp import create_app
from webapp.model import db, Content
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


def get_modified_date(string_date):
    date_dt = datetime.strptime(string_date[:-10], "%Y-%m-%d %H:%M")
    return date_dt

lesson_names = ["Learn Python", "Создадим отдельный модуль для получения новостей", "Соберем сниппеты с Хабрахабр", "Обработаем тексты новостей", "Рассмотрим страницы статей на сайте", "Познакомимся с Celery", "Узнаем про выполнение задач по расписанию", "Клавиатура для текстовых сообщений", "Клавиатура для сообщений с картинками", "Что такое тестирование и зачем оно нужно?", "Что и как тестировать?", "Инструменты тестирования кода"]
descriptions = ["Learn Python: Лекции 9 недели", "Создадим отдельный модуль для получения новостей", "Соберем сниппеты с Хабрахабр", "Обработаем тексты новостей", "Рассмотрим страницы статей на сайте", "Познакомимся с Celery", "Узнаем про выполнение задач по расписанию", "Клавиатура для текстовых сообщений", "Клавиатура для сообщений с картинками", "Тестирование", "Тестирование", "Тестирование"]
section_names = ["Learn Python: Лекции 9 недели", "Трек Веб-разработка", "Трек Веб-разработка", "Трек Веб-разработка", "Трек Веб-разработка", "Трек Веб-разработка", "Трек Веб-разработка", "Трек Боты", "Трек Боты", "Дополнительно", "Дополнительно", "Дополнительно"]
url_descriptions = ["", "Learn Python: Лекции 9 недели", "Learn Python: Лекции 9 недели", "Learn Python: Лекции 9 недели", "Learn Python: Лекции 9 недели", "Learn Python: Лекции 9 недели", "Learn Python: Лекции 9 недели", "Learn Python: Лекции 9 недели", "Learn Python: Лекции 9 недели", "Learn Python: как тестировать свой код. Лекции 8 недели", "Learn Python: как тестировать свой код. Лекции 8 недели", "Learn Python: как тестировать свой код. Лекции 8 недели"]
types_ = ["", "youtube_link", "youtube_link", "youtube_link", "youtube_link", "youtube_link", "youtube_link", "youtube_link", "youtube_link", "youtube_link", "youtube_link", "youtube_link"]
urls = ["text_14", "https://www.youtube.com/embed/YFgWRVKb-rI", "https://www.youtube.com/embed/b-byWpaEiww", "https://www.youtube.com/embed/KSOFq2v9pL4", "https://www.youtube.com/embed/8vmDTwiinEw", "https://www.youtube.com/embed/sF_SeAWDq0Y", "https://www.youtube.com/embed/8VdxSh2sOkk", "https://www.youtube.com/embed/DpCeCFIm4A4", "https://www.youtube.com/embed/rX7idZsnWfI", "https://www.youtube.com/embed/Mud-X6Q8uEA", "https://www.youtube.com/embed/YfDojwNa-7o", "https://www.youtube.com/embed/Sua7Oi6qsmk"]
slugs = ["", "modul-dlya-novostey", "modul-dlya-novostey", "modul-dlya-novostey", "modul-dlya-novostey", "modul-dlya-novostey", "modul-dlya-novostey", "klaviatura", "klaviatura", "testing", "testing", "testing"]
string_dates = ["2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000", "2019-10-26 16:25:00.000000"]


app = create_app()
with app.app_context():
     for lesson_name, description, section_name, url_description, type_, url, string_date, slug in zip(lesson_names, descriptions, section_names, url_descriptions, types_, urls, string_dates, slugs):
        modified_date = get_modified_date(string_date)
        content = Content(lesson_name=lesson_name, description=description, section_name=section_name, type=type_, url_description=url_description, url=url, modified_date=modified_date, slug=slug)
        db.session.add(content)
        db.session.commit()
    
    
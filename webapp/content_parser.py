import datetime
import requests
import re
import os
import json

from bs4 import BeautifulSoup as bso

from webapp.model import db, Content
from webapp.transliterator import get_slug

def get_html():
    basedir = os.path.abspath(os.path.dirname(__file__))
    basename = "datafile.txt"
    try:
        with open(f"{basedir}/{basename}", "r") as f:
            raw_text = f.read()
    except FileNotFoundError:
        return False
    
    html_list = re.findall(r"<html.*?</html>", raw_text, re.DOTALL)
    html = "".join(html_list)
    return html

def get_modified_date(title):
    basedir = os.path.abspath(os.path.dirname(__file__))
    basename = "meta_msg.json"
    with open(f"{basedir}/{basename}", "r") as f:
        msg_received_list = json.load(f)

    for msg in msg_received_list:
        if msg["subject"] == title:
            string_date = msg["received"]
            # date_dt = datetime.datetime.strptime(string_date[5:16], "%d %b %Y")
            date_dt = datetime.datetime.strptime(string_date[5:22], "%d %b %Y %H:%M")
            return date_dt

def get_text(body, m, n):
    table = body.find('table')
    # return table.get_text()[m:n]

    raw_text = ""
    for td in table.findChildren('td'):
        if td.text not in raw_text:
            raw_text += td.text
    text = raw_text[m:n]   # [31:-16]
    return text


def get_all_a_in_text(body, section_name, modified_date): # название чушь и не отражает сути решаемой задачи
    table = body.find('table')

    li_list_obj = body.find_all('li')
    li_lists_2d = [li.find_all('a') for li in li_list_obj if li.a]
    li_list = [li.text for li_list in li_lists_2d for li in li_list]

    web_match = re.compile(r".*web.*\.html.*")
    ds_match = re.compile(r".*ds.*\.html.*")
    bot_match = re.compile(r".*bot.*\.html.*")
    
    for a in table.find_all('a'):
        if a.text not in li_list:
            url, type = get_url_and_url_type(a)
            if web_match.search(url):
                lesson_name = "Трек Веб-программирование"
                description = lesson_name # ???
                url_description = a.text
                slug = get_slug_url(lesson_name, section_name)
                write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=url_description, type=type, slug=slug)
            elif ds_match.search(url):
                lesson_name = "Трек Data-Science"
                description = lesson_name # ???
                url_description = a.text
                slug = get_slug_url(lesson_name, section_name)
                write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=url_description, type=type, slug=slug)               
            elif bot_match.search(url):
                lesson_name = "Трек Telegram-bot"
                description = lesson_name # ???
                url_description = a.text
                slug = get_slug_url(lesson_name, section_name)
                write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=url_description, type=type, slug=slug)             
                
            else:

                url, type = get_url_and_url_type(a)
                lesson_name = section_name
                description = lesson_name # ???
                url_description = a.text
                slug = get_slug_url(lesson_name, section_name)
                write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=url_description, type=type, slug=slug)


def get_url_and_url_type(a):
    youtube_regex = re.compile(r"\S+\/")
    video_id_regex = re.compile(r"\?[^\&]*")

    raw_url = a['href']          
    description = a.text         
    if description != "ссылка на чат":
        try:
            response = requests.get(raw_url)
            response.raise_for_status()
            url = response.url
        except (requests.RequestException, ValueError) as e:
            print(f'[{e}] Network Error')
            url = f"[{e}] Couldn't get info for '{description}' due to connection issue"
            type = url
            return url, type
    else:
        url = "joinchat telegram link"

    if 'youtube' in url:
        type = "youtube_link"
        youtube = youtube_regex.search(url).group(0)
        video_id = video_id_regex.search(url).group(0)
        url = youtube + "embed/" + video_id[3:] 
    else:
        type = "external_link"
    return url, type  


def get_slug_url(lesson_name, section_name):
    if "пожаловать" not in section_name.lower():
        section_slug = get_slug(section_name.lower())
        theme_slug = get_slug(lesson_name.lower())
        if "kompleksnye" in theme_slug:
            theme_slug = "kompleksnye-tipy-dannyh"
        elif "prostye" in theme_slug:
            theme_slug = "prostye-tipy-dannyh"
        elif "pishem" in theme_slug:
            theme_slug = "pishem-bota-dlya-telegram"
        elif "virtualnoe" in theme_slug:
            theme_slug = "virtualnoe-okruzhenie"
        elif "tipichnyh" in theme_slug:
            theme_slug = "csv"
        elif theme_slug.endswith("-"):
            theme_slug = theme_slug[:-1]
        url_slug = theme_slug
        return url_slug
    else:
        return ""

def pretifier(lesson_name):
    match_symb_list = ["(", ":", "-", "."]
    result = []
    for symb in match_symb_list:
        if symb in lesson_name:
            if symb == "-" or symb == ".":
                idx = lesson_name.index(symb)
                result.append(lesson_name[:idx])
            elif symb == ":":
                idx = lesson_name.index(symb)
                result.append(lesson_name[:idx])
            elif symb == "(":
                idx = lesson_name.index(symb)
                result.append(lesson_name[:idx-1])
    
    if not result:
        return lesson_name
    
    if "списки" in lesson_name.lower() or "словари" in lesson_name.lower():
        return "Комплексные типы данных"
    elif "простые" in lesson_name.lower():
        return "Простые типы данных"
    elif "файлы" in lesson_name.lower():
        return "Файлы *.py и IDE"
    elif "повторять" in lesson_name.lower():
        return "Циклы for и while"
    elif "наработки" in lesson_name.lower():
        return "Модули"
    elif "исключения" in lesson_name.lower():
        return "Обработка исключений"
    elif "выбор" in lesson_name.lower():
        return "Условный оператор if"   
    elif "окружение" in lesson_name.lower():
        return "Виртуальное окружение"
    elif "с датой и временем" in lesson_name.lower():
        return "Работа с датой и временем"
    elif "работа с файлами" in lesson_name.lower():
        return "Работа с файлами"    
    elif "типичных применений" in lesson_name.lower():
        return "Табличный формат csv"
    elif "ООП" in lesson_name.lower():
        return "ООП в Python"
    return min(result)


def write_to_db(lesson_name, description, section_name, url, slug="", modified_date="Empty", url_description="Empty", type="text"):
    
    if "добро" in section_name.lower():
        check_columns_list = [lesson_name, description]
        if "Windows" in check_columns_list or "Mac OS" in check_columns_list or "Linux" in check_columns_list:
            return False

    url_exist = Content.query.filter(Content.url == url).count()
    if type == "text":
        url_description_exist = Content.query.filter(Content.url_description == url_description).count()
        print(f"description exist is {bool(url_description_exist)}")
        print(f"url_exist is {bool(url_exist)}")
        if not url_description_exist and not url_exist:
            content = Content(lesson_name=lesson_name, description=description, section_name=section_name, type=type, url_description=url_description, url=url, modified_date=modified_date, slug=slug)
            db.session.add(content)
            db.session.commit()
    else:
        print(f"url_exist is {bool(url_exist)}")
        if not url_exist:
            content = Content(lesson_name=lesson_name, description=description, section_name=section_name, type=type, url_description=url_description, url=url, modified_date=modified_date, slug=slug)
            db.session.add(content)
            db.session.commit()
        else:
            print(lesson_name + " | " + slug + " | " + url)

def get_content_entries(counter):
    html = get_html()
    if html:
        soup = bso(html, "html.parser")
        bodies = soup.find_all("body")

        titles = soup.find_all("title")         
        letters_body_list = []
        for idx, (body, title) in enumerate(zip(bodies, titles)):
            letter_dict = {
                "letter_number": idx,      # ex-letter_order
                "letter_title": title.text,
                "body": body
            }
            letters_body_list.append(letter_dict)

        wasted_letters_numbers = [2,4,8,16]
        without_li_letters_numbers = [6,7,10,11]
        strong_theme_letters = [5,9,12,13,14,15,17]

        for idx, letter in enumerate(letters_body_list):
            # for i in without_li_letters_numbers:
            #     print(letters_body_list[i]["letter_title"])
            # exit(0)
            # continue
            # letter = letters_body_list[10]
            # letter["letter_number"] = 12
            # letter["body"] = letters_body_list[12]["body"]
            # letter["letter_title"] = letters_body_list[12]["letter_title"]
            if letter["letter_number"] in wasted_letters_numbers:
                continue
            else:
                section_name = letter["letter_title"]
                modified_date = get_modified_date(section_name)   

                get_all_a_in_text(letter["body"], letter["letter_title"], modified_date)

                # # text = get_text(letter["body"], 31, -16)
                description = section_name
                lesson_name = pretifier(section_name)
                url = "text_" + str(counter)
                counter += 1
                write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=str(letter["body"]))
                

                if letter["letter_number"] == 5: # виртуальное окружение
                    ol = letter["body"].find('ol')
                    for li in ol.find_all('li'):
                        list_a = li.find_all('a')
                        for a in list_a:
                            description = li.text
                            lesson_name = pretifier(li.text)
                            section_name = letter["letter_title"]
                            url_description = a.text
                            url, type = get_url_and_url_type(a)
                            slug = get_slug_url(lesson_name, section_name) # возможно стоит передавать description вместо lesson_name. Проверить!
                            write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=url_description, type=type, slug=slug)


                if letter["letter_number"] in strong_theme_letters: # недели 4,5,6,7,8 (тесты), 9
                    strongs = letter["body"].find_all("strong")
                    for strong in strongs:
                        next_ = strong.find_next()
                        if next_.li:
                            li_list = next_.find_all("li")
                            for li in li_list:
                                section_name = strong.text
                                lesson_name = pretifier(li.text)
                                description = li.text
                                url_description = letter["letter_title"]
                                url, type = get_url_and_url_type(li.a)
                                slug = get_slug_url(lesson_name, section_name) # возможно стоит передавать description вместо lesson_name. Проверить!
                                write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=url_description, type=type, slug=slug)
                        elif "проекты" in strong.text.lower(): 
                            next_next_ = next_.find_next().find_next()
                            section_name = letter["letter_title"]
                            url_description = next_next_.text
                            lesson_name = pretifier(strong.text)
                            description = strong.text
                            url, type = get_url_and_url_type(next_next_)
                            slug = get_slug_url(lesson_name, section_name) # возможно стоит передавать description вместо lesson_name. Проверить!
                            write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=url_description, type=type, slug=slug)

                            next_next_next_ = next_next_.find_next()
                            section_name = letter["letter_title"]
                            url_description = next_next_next_.text
                            description = strong.text
                            lesson_name = pretifier(strong.text)
                            url, type = get_url_and_url_type(next_next_next_)
                            slug = get_slug_url(lesson_name, section_name) # возможно стоит передавать description вместо lesson_name. Проверить!
                            write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=url_description, type=type, slug=slug)
                        elif "трек" in strong.text.lower() or "дополнительно" in strong.text.lower():
                            # continue
                            if "5-й недели" in letter["letter_title"].lower() or "9 недели" in letter["letter_title"].lower():
                                next_next_ = next_.find_next().find_next().find_next()
                            elif "трек" in strong.text.lower():
                                next_next_ = next_.find_next().find_next()
                            elif "дополнительно" in strong.text.lower():
                                next_next_ = next_.find_next()
                            li_list = next_next_.find_all("li")
                            for li in li_list:
                                section_name = strong.text.replace('"', '')
                                lesson_name = pretifier(li.text)
                                description = li.text
                                url_description = letter["letter_title"]
                                url, type = get_url_and_url_type(li.a)
                                slug = get_slug_url(lesson_name, section_name) # возможно стоит передавать description вместо lesson_name. Проверить!
                                write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=url_description, type=type, slug=slug)

                elif letter["letter_number"] in without_li_letters_numbers: # Trello, проекты, доп задания
                    lesson_name = pretifier(section_name)
                    description = section_name
                    regex = re.compile(r".*gmail.com.*|.*subscri*.|why did I get this")
                    tables = letter["body"].find_all("table")
                    for td in tables:
                        list_a = td.find_all('a')
                        for a in list_a:
                            match = regex.search(a.text)
                            if not match:                            
                                url, type = get_url_and_url_type(a)
                                url_description = a.text       
                                slug = get_slug_url(lesson_name, section_name)  # возможно стоит передавать description вместо lesson_name. Проверить!
                                write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, type=type, url_description=url_description, slug=slug)
                
                else:
                    # недели: 0(приветственное), 1, 2

                    # text = get_text(letter["body"], 31, -16)
                    # theme_name = section_name
                    # url = "text_" + str(counter)
                    # counter += 1
                    # slug = get_slug_url(theme_name, section_name)
                    # write_to_db(theme_name, section_name, url, modified_date=modified_date, description=str(letter["body"]), slug=slug)

                    # continue

                    li_els = letter["body"].find_all('li')
                    for li in li_els:
                        if li.a:
                            a_els = li.find_all('a')
                            for a in a_els:
                                lesson_name = pretifier(li.text)
                                description = li.text
                                url_description = a.text
                                url, type = get_url_and_url_type(a)
                                slug = get_slug_url(lesson_name, section_name) # возможно стоит передавать description вместо lesson_name. Проверить!
                                write_to_db(lesson_name, description, section_name, url, modified_date=modified_date, url_description=url_description, type=type, slug=slug)
    else:
        print('\t[Error] No datafile found')   

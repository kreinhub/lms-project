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


def get_all_a_in_text(body, section_name, modified_date):
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
                theme_name = "Трек Веб-программирование"
                description = a.text
                write_to_db(theme_name, section_name, url, modified_date=modified_date, description=description, type=type)
            elif ds_match.search(url):
                theme_name = "Трек Data-Science"
                description = a.text
                write_to_db(theme_name, section_name, url, modified_date=modified_date, description=description, type=type)               
            elif bot_match.search(url):
                theme_name = "Трек Telegram-bot"
                description = a.text
                write_to_db(theme_name, section_name, url, modified_date=modified_date, description=description, type=type)             
                
            else:

                url, type = get_url_and_url_type(a)
                theme_name = section_name
                description = a.text
                write_to_db(theme_name, section_name, url, modified_date=modified_date, description=description, type=type)


def get_url_and_url_type(a):
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
    else:
        type = "external_link"
    return url, type  


def get_slug_url(theme_name, section_name):
    # if "text" in url:
    if "пожаловать" not in section_name.lower():
        section_slug = get_slug(section_name.lower())
        theme_slug = get_slug(theme_name.lower())
        if "kompleksnye" in theme_slug:
            theme_slug = "kompleksnye-tipy-dannyh"
        elif "prostye" in theme_slug:
            theme_slug = "prostye-tipy-dannyh"
        elif "pishem" in theme_slug:
            theme_slug = "pishem-bota-dlya-telegram"
        # elif "povtoryat" in theme_slug:
        #     theme_slug = "cycles"
        elif "virtualnoe" in theme_slug:
            theme_slug = "virtualnoe-okruzhenie"
        elif "tipichnyh" in theme_slug:
            theme_slug = "csv"
        elif theme_slug.endswith("-"):
            theme_slug = theme_slug[:-1]
        # url_slug = "/" + section_slug + "/" + theme_slug + "/"
        # url_slug = theme_slug + "/"
        url_slug = theme_slug
        return url_slug
    else:
        return ""

def pretifier(theme_name):
    match_symb_list = ["(", ":", "-", "."]
    result = []
    for symb in match_symb_list:
        if symb in theme_name:
            if symb == "-" or symb == ".":
                idx = theme_name.index(symb)
                result.append(theme_name[:idx])
            elif symb == ":":
                idx = theme_name.index(symb)
                result.append(theme_name[:idx])
            elif symb == "(":
                idx = theme_name.index(symb)
                result.append(theme_name[:idx-1])
    
    if not result:
        return theme_name
    
    if "списки" in theme_name.lower() or "словари" in theme_name.lower():
        return "Комплексные типы данных"
    elif "простые" in theme_name.lower():
        return "Простые типы данных"
    elif "файлы" in theme_name.lower():
        return "Файлы *.py и IDE"
    elif "повторять" in theme_name.lower():
        return "Циклы for и while"
    elif "наработки" in theme_name.lower():
        return "Модули"
    elif "исключения" in theme_name.lower():
        return "Обработка исключений"
    elif "выбор" in theme_name.lower():
        return "Условный оператор if"   

    return min(result)


def write_to_db(theme_name, section_name, url, slug="", modified_date="Empty", description="Empty", type="text"):
    
    url_exist = Content.query.filter(Content.url == url).count()
    if type == "text":
        description_exist = Content.query.filter(Content.description == description).count()
        print(f"description exist is {bool(description_exist)}")
        print(f"url_exist is {bool(url_exist)}")
        if not description_exist and not url_exist:
            content = Content(theme_name=theme_name, section_name=section_name, type=type, description=description, url=url, modified_date=modified_date, slug=slug)
            db.session.add(content)
            db.session.commit()
    else:
        print(f"url_exist is {bool(url_exist)}")
        if not url_exist:
            content = Content(theme_name=theme_name, section_name=section_name, type=type, description=description, url=url, modified_date=modified_date, slug=slug)
            db.session.add(content)
            db.session.commit()


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

                list_a_in_text = get_all_a_in_text(letter["body"], letter["letter_title"], modified_date)

                # # text = get_text(letter["body"], 31, -16)
                theme_name = section_name
                url = "text_" + str(counter)
                counter += 1
                # # write_to_db(theme_name, section_name, modified_date=modified_date, description=text, url=url)
                write_to_db(theme_name, section_name, url, modified_date=modified_date, description=str(letter["body"]))
                

                if letter["letter_number"] == 5: # виртуальное окружение
                    # continue

                    ol = letter["body"].find('ol')
                    for li in ol.find_all('li'):
                        list_a = li.find_all('a')
                        for a in list_a:
                            theme_name = li.text
                            section_name = letter["letter_title"]
                            description = a.text
                            url, type = get_url_and_url_type(a)
                            slug = get_slug_url(theme_name, section_name)
                            write_to_db(theme_name, section_name, url, modified_date=modified_date, description=description, type=type, slug=slug)


                if letter["letter_number"] in strong_theme_letters: # недели 4,5,6,7,8 (тесты), 9
                    # continue

                    strongs = letter["body"].find_all("strong")
                    for strong in strongs:
                        next_ = strong.find_next()
                        if next_.li:
                            # continue

                            li_list = next_.find_all("li")
                            for li in li_list:
                                section_name = strong.text
                                theme_name = li.text
                                description = letter["letter_title"]
                                url, type = get_url_and_url_type(li.a)
                                slug = get_slug_url(theme_name, section_name)
                                write_to_db(theme_name, section_name, url, modified_date=modified_date, description=description, type=type, slug=slug)
                        elif "проекты" in strong.text.lower(): 
                            # continue

                            next_next_ = next_.find_next().find_next()
                            section_name = letter["letter_title"]
                            description = next_next_.text
                            theme_name = strong.text
                            url, type = get_url_and_url_type(next_next_)
                            slug = get_slug_url(theme_name, section_name)
                            write_to_db(theme_name, section_name, url, modified_date=modified_date, description=description, type=type, slug=slug)

                            next_next_next_ = next_next_.find_next()
                            section_name = letter["letter_title"]
                            description = next_next_next_.text
                            theme_name = strong.text
                            url, type = get_url_and_url_type(next_next_next_)
                            slug = get_slug_url(theme_name, section_name)
                            write_to_db(theme_name, section_name, url, modified_date=modified_date, description=description, type=type, slug=slug)
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
                                theme_name = li.text
                                description = letter["letter_title"]
                                url, type = get_url_and_url_type(li.a)
                                slug = get_slug_url(theme_name, section_name)
                                write_to_db(theme_name, section_name, url, modified_date=modified_date, description=description, type=type, slug=slug)
                elif letter["letter_number"] in without_li_letters_numbers: # Trello, проекты, доп задания
                    # continue

                    theme_name = section_name
                    regex = re.compile(r".*gmail.com.*|.*subscri*.|why did I get this")
                    tables = letter["body"].find_all("table")
                    for td in tables:
                        list_a = td.find_all('a')
                        for a in list_a:
                            match = regex.search(a.text)
                            if not match:                            
                                url, type = get_url_and_url_type(a)
                                description = a.text       
                                slug = get_slug_url(theme_name, section_name)
                                write_to_db(theme_name, section_name, url, modified_date=modified_date, type=type, description=description, slug=slug)
                
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

                                # theme_name = li.text
                                theme_name = pretifier(li.text)
                                description = a.text
                                url, type = get_url_and_url_type(a)
                                slug = get_slug_url(theme_name, section_name)
                                write_to_db(theme_name, section_name, url, modified_date=modified_date, description=description, type=type, slug=slug)
    else:
        print('\t[Error] No datafile found')   

if __name__ == "__main__":
    print(get_content_entries())
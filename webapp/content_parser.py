import datetime
import requests
import re
import os
import json

from bs4 import BeautifulSoup as bso

from webapp.model import db, Content


def get_html():
    basedir = os.path.abspath(os.path.dirname(__file__))
    basename = "datafile.txt"
    try:
        with open(f"{basedir}/{basename}", "r") as f:
            raw_text = f.read()
    except FileNotFoundError:
        return False
    soup = bso(raw_text, "html.parser")
    object_html = soup.find_all('html')
    list_html = [str(item) for item in object_html]    
    html = '\n'.join(list_html)

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
                write_to_db(theme_name, section_name, modified_date=modified_date, description=description, url=url, type=type)
            elif ds_match.search(url):
                theme_name = "Трек Data-Science"
                description = a.text
                write_to_db(theme_name, section_name, modified_date=modified_date, description=description, url=url, type=type)               
            elif bot_match.search(url):
                theme_name = "Трек Telegram-bot"
                description = a.text
                write_to_db(theme_name, section_name, modified_date=modified_date, description=description, url=url, type=type)             
                
            else:

                url, type = get_url_and_url_type(a)
                theme_name = section_name
                description = a.text
                write_to_db(theme_name, section_name, modified_date=modified_date, description=description, url=url, type=type)


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


def write_to_db(theme_name, section_name, modified_date="Empty", description="Empty", type="text", url="Empty"):
    
    url_exist = Content.query.filter(Content.url == url).count()
    if type == "text":
        description_exist = Content.query.filter(Content.description == description).count()
        print(f"description exist is {description_exist}")
        print(f"url_exist is {url_exist}")
        if not description_exist and not url_exist:
            content = Content(theme_name=theme_name, section_name=section_name, type=type, description=description, url=url, modified_date=modified_date)
            db.session.add(content)
            db.session.commit()
    else:
        print(f"url_exist is {url_exist}")
        if not url_exist:
            content = Content(theme_name=theme_name, section_name=section_name, type=type, description=description, url=url, modified_date=modified_date)
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

        wasted_letters_numbers = [2,4,8]
        without_li_letters_numbers = [6, 7, 10, 11]
        strong_theme_letters = [5, 9, 12, 13, 14]

        for idx, letter in enumerate(letters_body_list):
            # letter["letter_number"] = 14
            # letter["body"] = letters_body_list[14]["body"]
            if letter["letter_number"] in wasted_letters_numbers:
                continue
            else:
                
                section_name = letter["letter_title"]
                modified_date = get_modified_date(section_name)   

                list_a_in_text = get_all_a_in_text(letter["body"], letter["letter_title"], modified_date)
                # continue

                text = get_text(letter["body"], 31, -16)
                theme_name = section_name
                url = "text_" + str(counter)
                counter += 1
                write_to_db(theme_name, section_name, modified_date=modified_date, description=text, url=url)
                
                if letter["letter_number"] == 5:
                    # continue

                    ol = letter["body"].find('ol')
                    for li in ol.find_all('li'):
                        list_a = li.find_all('a')
                        for a in list_a:
                            theme_name = li.text
                            section_name = letter["letter_title"]
                            description = a.text
                            url, type = get_url_and_url_type(a)
                            write_to_db(theme_name, section_name, modified_date=modified_date, description=description, url=url, type=type)


                if letter["letter_number"] in strong_theme_letters:
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
                                write_to_db(theme_name, section_name, modified_date=modified_date, description=description, url=url, type=type)
                        elif "проекты" in strong.text.lower(): 
                            # continue

                            next_next_ = next_.find_next().find_next()
                            section_name = letter["letter_title"]
                            description = next_next_.text
                            theme_name = strong.text
                            url, type = get_url_and_url_type(next_next_)
                            write_to_db(theme_name, section_name, modified_date=modified_date, description=description, url=url, type=type)

                            next_next_next_ = next_next_.find_next()
                            section_name = letter["letter_title"]
                            description = next_next_next_.text
                            theme_name = strong.text
                            url, type = get_url_and_url_type(next_next_next_)
                            write_to_db(theme_name, section_name, modified_date=modified_date, description=description, url=url, type=type)
                        elif "трек" in strong.text.lower() or "дополнительно" in strong.text.lower():
                            # continue

                            if "трек" in strong.text.lower():
                                next_next_ = next_.find_next().find_next()
                            elif "дополнительно" in strong.text.lower():
                                next_next_ = next_.find_next()
                            li_list = next_next_.find_all("li")
                            for li in li_list:
                                section_name = strong.text
                                theme_name = li.text
                                description = letter["letter_title"]
                                url, type = get_url_and_url_type(li.a)
                                write_to_db(theme_name, section_name, modified_date=modified_date, description=description, url=url, type=type)
                elif letter["letter_number"] in without_li_letters_numbers:
                    # continue

                    theme_name = section_name
                    regex = re.compile(r".*gmail.com.*|.*subscri*.|why did I get this")
                    tables = letter["body"].find_all("table")
                    uniq_check_list = []   # нужен только для проверки уникальности
                    for td in tables:
                        list_a = td.find_all('a')
                        for a in list_a:
                            match = regex.search(a.text)
                            if a.text not in uniq_check_list and not match:
                                url, type = get_url_and_url_type(a)
                                description = a.text                       
                                write_to_db(theme_name, section_name, modified_date=modified_date, type=type, url=url, description=description)
                                uniq_check_list.append(a.text)
                
                else:
                    # continue
                    
                    text = get_text(letter["body"], 31, -16)
                    theme_name = section_name
                    url = "text_" + str(counter)
                    counter += 1
                    write_to_db(theme_name, section_name, modified_date=modified_date, description=text, url=url)

                    # continue

                    li_els = letter["body"].find_all('li')
                    for li in li_els:
                        if li.a:
                            a_els = li.find_all('a')
                            for a in a_els:
                                theme_name = li.text
                                description = a.text
                                url, type = get_url_and_url_type(a)
                                write_to_db(theme_name, section_name, modified_date=modified_date, description=description, url=url, type=type)

# get_content_entries(1)      
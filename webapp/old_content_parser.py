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

# i = 0
# for r in rows:
#     # insert row
#     if i % 100 == 0:
#         # commit
#         pass
#     i+=1
# # commit

def write_to_db(theme_name, section_name, modified_date="Empty", description="Empty", type="text", url="Empty"):
    
    content_exist = Content.query.filter(Content.url == url).count()
    print(content_exist)
    if not content_exist:
        content = Content(theme_name=theme_name, section_name=section_name, type=type, description=description, url=url, modified_date=modified_date)
        db.session.add(content)
        db.session.commit()
    # else:
    #     print(f"\t{theme_name}\n\t{url}\n\t{description}")


def get_modified_date(section_name):
    basedir = os.path.abspath(os.path.dirname(__file__))
    basename = "meta_msg.json"
    with open(f"{basedir}/{basename}", "r") as f:
        msg_received_list = json.load(f)

    for msg in msg_received_list:
        if msg["subject"] == section_name:
            string_date = msg["received"]
            # date_dt = datetime.datetime.strptime(string_date[5:16], "%d %b %Y")
            date_dt = datetime.datetime.strptime(string_date[5:22], "%d %b %Y %H:%M")
            return date_dt

def get_url_type_description(a):
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
            return url, type, description
        # hostname = urlparse(response.url).netloc
        # print(hostname)
    else:
        url = "joinchat telegram link"

    if 'youtube' in url:
        type = "youtube_link"
    else:
        type = "external_link"
    return url, type, description


def write_common_fields(body, section_name, modified_date):
    li_els = body.find_all('li')
    for li in li_els:
        if li.a:
            a_els = li.find_all('a')
            for a in a_els:
                theme_name = li.text
                url, type, description = get_url_type_description(a)
                write_to_db(theme_name, section_name, modified_date=modified_date, type=type, url=url, description=description)


def get_description(body, m, n):
    table = body.find('table')
    raw_text = ""
    for td in table.findChildren('td'):
        if td.text not in raw_text:
            raw_text += td.text
    description = raw_text[m:n]   # [31:-16]
    return description


def get_content_entries(counter):
    html = get_html()
    if html:
        soup = bso(html, "html.parser")
        bodies = soup.find_all("body")

        titles = soup.find_all("title")         
        sections_body_list = []
        for idx, (body, title) in enumerate(zip(bodies, titles)):
            section_dict = {
                "section_number": idx,      # ex-letter_order
                "section_name": title.text,
                "body": body
            }
            sections_body_list.append(section_dict)

        wasted_letters_numbers = [2,4,8]
        without_li_letters_numbers = [6, 7, 10, 11]
        for section in sections_body_list:
            if section["section_number"] in wasted_letters_numbers:
                continue
            else:
                # Here we get text type
                modified_date = get_modified_date(section["section_name"])
                section_name = section["section_name"]
                description = get_description(section["body"], 31, -16)
                # if a_in_text():
                #   do smth
                # else: 
                url = "text_" + str(counter)
                counter += 1
                write_to_db(section_name, section_name, modified_date, description, type="text", url=url)
                
                if section["section_number"] not in without_li_letters_numbers:
                    # Here we get all content types for all letters with li and write them into db
                    write_common_fields(section["body"], section_name, modified_date) 
                    
                else:
                    # Here we get all content types for all letters WITHOUT li and write them into db
                    theme_name = section_name
                    regex = re.compile(r".*gmail.com.*|.*subscri*.|why did I get this")
                    tables = section["body"].find_all("table")
                    uniq_check_list = []   # нужен только для проверки уникальности
                    for td in tables:
                        list_a = td.find_all('a')
                        for a in list_a:
                            match = regex.search(a.text)
                            if a.text not in uniq_check_list and not match:
                                url, type, description = get_url_type_description(a)                       
                                write_to_db(theme_name, section_name, modified_date=modified_date, type=type, url=url, description=description)
                                uniq_check_list.append(a.text)

# from datetime import datetime
import requests
import json
import re
import os

from bs4 import BeautifulSoup as bso


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

def get_description(body, m, n):
    # Here we get description field for text
    table = body.find('table')
    raw_text = ""
    for td in table.findChildren('td'):
        if td.text not in raw_text:
            raw_text += td.text
    description = raw_text[m:n]   # [31:-16]
    return description


def write_to_json(theme_name, section_name, modified_date="Empty", description="Empty", type="list_of_links", url="text"):
    new_entry_dict = {
        "theme_name": theme_name,
        "section_name": section_name,
        "description": description,
        "type": type,
        "url": url,
        "modified_date": modified_date
    }
    with open("content_store.json", "r") as f:
        current_storage = json.load(f)
    
    if new_entry_dict not in current_storage:
        current_storage.append(new_entry_dict)
        with open("content_store.json", "w+") as f:
            f.write(json.dumps(current_storage, ensure_ascii=False))


def main():
    html = get_html()
    soup = bso(html, "html.parser")
    bodies = soup.find_all("body")
    
    # for body in bodies:            # НЕ УДАЛЯТЬ! 
    #     ols = body.find_all('ol')
    #     for li in ols:
    #         print(li)

    titles = soup.find_all("title")         
    sections_body_list = []
    for idx, (body, title) in enumerate(zip(bodies, titles)):
        section_dict = {
            "section_number": idx,      # ex-letter_order
            "section_name": title.text,
            "body": body
        }
        sections_body_list.append(section_dict)
    # print(sections_body_list)
    for section in sections_body_list:
        if section["section_number"] == 0:   # Добро пожаловать
            # Here we get modified_date
            # modified_date = datetime.strptime('02/09/19', "%d/%m/%y")
            modified_date = "2019-09-02"
            # Here we get section_name field
            section_name = section["section_name"]
            # Here we get description field
            description = get_description(section["body"], 34, -31)
            # Here we get the common fields
            uls = section["body"].find_all('ul')
            ols = section["body"].find_all('ol')

            write_to_json(section_name, section_name, modified_date, description, type="text")
            for li_ul, li_ol in zip(uls, ols):
                if li_ul.a:
                    theme_name = li_ul.text
                    object_urls = li_ul.find_all('a')
                    list_urls = [str(url) for url in object_urls]    
                    write_to_json(theme_name, section_name, modified_date, url=list_urls)
                    # print(theme_name)
                    # print(urls)
                if li_ol.a:
                    theme_name = li_ol.text
                    object_urls = li_ol.find_all('a')
                    list_urls = [str(url) for url in object_urls]    
                    write_to_json(theme_name, section_name, modified_date, url=list_urls)
                    # print(theme)
                    # print(urls)
        elif section["section_number"] == 2 or section["section_number"] == 4 or section["section_number"] == 8: # Запись созвона, второе ненужное письмо в цепочке "Learn Python: Материал 2 недели" и про изменение площадки
            # print(section["section_name"])
            continue 

        elif 0 < section["section_number"] < 4:
            # Here we get modified_date
            if section["section_number"] == 1:
                modified_date = "2019-09-07"
            else:                              # номер 3 "Материал второй недели"
                modified_date = "2019-09-08"
            # Here we get section_name field
            section_name = section["section_name"]
            # Here we get description field for text
            description = get_description(section["body"], 31, -16)
            write_to_json(section_name, section_name, modified_date, description, type="text")

            # Here we get the common fields
            li_list = section["body"].find('ul').find_all('li')
            for li in li_list:
                theme_name = li.text
                list_a = li.find_all('a')
                for a in list_a:
                    raw_url = a['href']
                    description = a.text
                    response = requests.get(raw_url)
                    url = response.url
                    if 'youtube' in url:
                        type = "youtube_link"
                    else:
                        type = "external_link"
                    write_to_json(theme_name, section_name, modified_date=modified_date, type=type, url=url, description=description)

        elif 5 < section["section_number"] < 8 or 9 < section["section_number"] < 12:  # 6, 7, 10 и 11 это не материалы, а что-то другое. 5 это виртуальное окружение...
            # print(section["section_name"])
            if section["section_number"] == 6:
                modified_date = "2019-09-15"
            elif section["section_number"] == 7:
                modified_date = "2019-09-17"
            elif section["section_number"] == 9:
                modified_date = "2019-09-28"
            
            # Here we get section name field
            section_name = section["section_name"]
            # Here we get description field for text and write it to json
            description = get_description(section["body"], 31, -16)     # 31 и -16 управляем срезом строки
            write_to_json(section_name, section_name, modified_date, description, type="text")
            # Here we get common fields
            theme_name = section_name
            
            regex = re.compile(r".*gmail.com.*|.*subscri*.|why did I get this")
            tables = section["body"].find_all("table")
            uniq_check_list = []   # нужен только для проверки уникальности
            for td in tables:
                list_a = td.find_all('a')
                for a in list_a:
                    match = regex.search(a.text)
                    if a.text not in uniq_check_list and not match:
                        description = a.text
                        raw_url = a["href"]
                        response = requests.get(raw_url)
                        url = response.url
                        if 'youtube' in url:
                            type = "youtube_link"
                        else:
                            type = "external_link"
                        write_to_json(theme_name, section_name, modified_date=modified_date, type=type, url=url, description=description)
                        uniq_check_list.append(a.text)
            # print(uniq_check_list)   


        else:                                       
            # print(section["section_name"])
            if section["section_number"] == 5:
                modified_date = "2019-09-14"
            elif section["section_number"] == 9:
                modified_date = "2019-09-21"
            elif section["section_number"] == 12:
                modified_date = "2019-09-28"
            elif section["section_number"] == 13:
                modified_date = "2019-10-05"

            # Here we get section name field
            section_name = section["section_name"]
            # Here we get description field for text
            description = get_description(section["body"], 31, -16)
            write_to_json(section_name, section_name, modified_date, description, type="text")

            # Here we get the common fields
            ols = section["body"].find_all('ol')
            for li in ols:
                theme_name = li.text
                list_a = li.find_all('a')
                for a in list_a:
                    raw_url = a['href']
                    description = a.text
                    response = requests.get(raw_url)
                    url = response.url
                    if 'youtube' in url:
                        type = "youtube_link"
                    else:
                        type = "external_link"
                    write_to_json(theme_name, section_name, modified_date=modified_date, type=type, url=url, description=description)



if __name__ == "__main__":
    main()
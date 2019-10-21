from datetime import datetime

import requests
from bs4 import BeautifulSoup
import json

from webapp.model import db, Articles


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Network Error")
        return False

def get_habr():
    html = get_html("https://habr.com/ru/hub/python/top/")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_arts = soup.findAll("h2", class_="post__title")
        all_arts_meta = soup.findAll("header", class_="post__meta")
        for art, meta in zip(all_arts, all_arts_meta):
            title = art.find('a').text
            url = art.find('a')['href']
            published = meta.find('span', class_="post__time")
            source = "habr"
            try:
                published = datetime.strptime(str(published), "%Y-%m-%d")
            except ValueError:
                published = datetime.now()
            
            save_to_db(title, url, published, source)
            # print(json.dumps({
            # "title": title,
            # "url": url,
            # "published": str(published)
            # }, indent=4, ensure_ascii=False))
    else:
        print("No")


def get_tproger():
    html = get_html("https://tproger.ru/tag/python/")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_arts_title = soup.findAll("h2", class_="entry-title")
        all_arts_content = soup.findAll("div", class_="entry-content")
        all_arts_img = soup.findAll("div", class_="entry-icon")
        all_urls = soup.findAll("a", class_="article-link")

        for idx, (title, content, url, img) in enumerate(zip(all_arts_title, all_arts_content, all_urls, all_arts_img)):
            title = title.text
            url = url["href"]
            try:
                text = content.p.text 
            except AttributeError:
                text = all_arts_content[idx+1].p.text
            img_src = img.find("img")["data-src"]
            published = datetime.now()
            source= "tproger"

            save_to_db(title, url, published, source, text, img_src)
            # print(json.dumps({
            # "title": title,
            # "url": url,
            # "text": text,
            # "img_src": img_src,
            # "published": published
            # }, indent=4, ensure_ascii=False))
    else:
        print("No")


def save_to_db(title, url, published, source, text="Empty", img_src="Empty"):
    art_exist = Articles.query.filter(Articles.url == url).count()
    print(art_exist)
    if not art_exist:
        news_news = Articles(title=title, url=url, text=text, published=published, img_url=img_src, source=source)
        db.session.add(news_news)
        db.session.commit()
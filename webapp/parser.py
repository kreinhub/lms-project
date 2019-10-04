from bs4 import BeautifulSoup
import re


def get_html():
    try:
        with open("datafile.txt", "r") as f:
            html = f.read()
    except FileNotFoundError:
        return False

    return html

def get_all_text():
    html = get_html()
    if html:
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table", class_="mcnTextContentContainer")
        all_text = ""
        for table in tables:
            for td in table.findChildren('td'):
                all_text += td.text
        return all_text
    else:
        raise FileNotFoundError

def get_all_links():
    html = get_html()
    if html:
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")
        
        all_links = []
        wasted_line = "why did I get this?"
        for link in links:
            email_match = re.search(r".*gmail.com.*", link.text)
            subscri_match =  re.search(r".*subscri*.", link.text)
            wasted_line = "why did I get this?"
            if not email_match and not subscri_match and link.text != wasted_line:
                all_links.append({link.text: link["href"]})
        return all_links
    else:
        raise FileNotFoundError


if __name__ == "__main__":
    try:
        all_text = get_all_text()
        all_links = get_all_links()
    except FileNotFoundError:
        print("\t[Error occured] Data file doesn't exist. Get it first")


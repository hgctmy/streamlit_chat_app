import requests
from bs4 import BeautifulSoup
import re


def topnews():
    url = "https://news.yahoo.co.jp/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    rs = soup.find_all(href=re.compile('news.yahoo.co.jp/pickup'))
    titles = []
    texts = []
    for i in rs:
        titles.append(i.getText())
        summary = requests.get(i.attrs['href'])
        summary_soup = BeautifulSoup(summary.text, "html.parser")
        summary_soup_a = summary_soup.select("a:contains('記事全文を読む')")[0]
        news_body_link = summary_soup_a.find()
        news_body = requests.get(news_body_link)
        news_soup = BeautifulSoup(news_body.text, "html.parser")
        texts.append(news_soup.title.text)
    return titles, texts


if __name__ == "__main__":
    print(topnews())

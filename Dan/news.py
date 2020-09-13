#!/usr/bin/env python3
import feedparser
from bs4 import BeautifulSoup
import requests
from datetime import datetime

startTime = datetime.now()

import psycopg2

count=0
#connect to db

con=psycopg2.connect(
    host='localhost',
    database="news",
    user='postgres',
    password='Redbox19!',
)

#cursor
cur=con.cursor()


count=0
cur.execute("SELECT article_link FROM news_list")
rows=cur.fetchall()

current_links_list=[r[0] for r in rows]
rss_dict = {}
rssurls = ['https://www.theguardian.com/uk/rss',
           'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
           'https://fivethirtyeight.com/all/feed',
           'http://feeds.feedburner.com/TechCrunch/',
           'https://thehill.com/rss/syndicator/19109',
           'https://www.aljazeera.com/xml/rss/all.xml',
           'https://www.scmp.com/rss/91/feed',
           'https://www.theatlantic.com/feed/all/',
           'https://rss.politico.com/politics-news.xml',
           'https://xml.euobserver.com/rss.xml',
           'http://feeds.bbci.co.uk/news/rss.xml',
           'http://feeds.arstechnica.com/arstechnica/index',
           'https://www.wired.com/feed/rss',
                ]
for urls in rssurls:
    d = feedparser.parse(urls)
    for post in d.entries:
        url = post.link
        if url in current_links_list:
            #print(f"{url} already exists")
            continue
        #print(f"{url} new article")



        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html, 'html5lib')
        article = soup.find_all('p')
        article_text = ' '.join([url.text for url in article])

        if post.published[0].isalpha():
            try:
                date=datetime.strptime(post.published,'%a, %d %b %Y %H:%M:%S %Z').strftime("%Y-%m-%d %n %H:%M:%S")
            except Exception as e:
                try:
                    date=datetime.strptime(post.published[:-6],'%a, %d %b %Y %H:%M:%S').strftime("%Y-%m-%d %n %H:%M:%S")
                except:
                    pass


            #print(f"converted from {post.published} to {date}")

        else:
            date=post.published

        rss_dict.update(
                {post.link:
                {'base_url': d.feed.link,
                'headline': post.title,
                'article_link': post.link,
                'author': post.get('author','Author not found'),
                'published_date':date,
                'article_text': article_text
            }})




d = list(rss_dict.values())

for post in d:
    cur.execute("insert into news_list (base_url,headline,article_link,author,published_date,article_text) values (%s,%s,%s,%s,%s,%s)",(post.get('base_url'),post.get('headline'),post.get('article_link'),post.get('author'),post.get('published_date'),post.get('article_text')))
    con.commit()
    count+=1





with open("sample.txt", "a") as file_object:

    # Append 'hello' at the end of file
    file_object.write("\n")
    file_object.write(f"Added {count} articles in about {datetime.now() - startTime}")


con.close()



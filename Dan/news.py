#!/usr/bin/env python3
import feedparser
from bs4 import BeautifulSoup
import requests
from gensim.summarization import summarize


from datetime import datetime

startTime = datetime.now()

import psycopg2

count=0
#connect to db

con=psycopg2.connect(
    host='localhost',
    database="news",
    user='postgres',
    password='admin',
)

#cursor
cur=con.cursor()


count=0
cur.execute("SELECT article_link FROM news_list")
rows=cur.fetchall()

current_links_list=[r[0] for r in rows]
rss_dict = {}
rssurls = [
    'https://www.theguardian.com/uk/rss',
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
            print(f"{url} already exists")
            continue
        print(f"{url} new article")



        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html, 'html5lib')
        article = soup.find_all('p')
        article_text = ' '.join([url.text for url in article])
        try:

            summary=summarize(article_text,ratio=0.04,word_count=50)
        except:
            try:
                summary=summarize(article_text,word_count=50)
            except:

                summary=article_text


        if post.published[0].isalpha():
            try:
                #***** for scmp articles with 8hours in advance***
                #get a dattime object so we can use datetime attributes
                date=datetime.strptime(post.published,'%a, %d %b %Y %H:%M:%S %z')

                #.utcoffset() returns the timedelta which means the delay and since both are datetime objects we can substract them to get the utc time
                c=date-date.utcoffset()


                #reconvert the datetime object to the wished format string to be added in the db
                date=c.strftime("%Y-%m-%d %n %H:%M:%S")
            except Exception as e:
                try:
                    date=datetime.strptime(post.published,'%a, %d %b %Y %H:%M:%S %Z').strftime("%Y-%m-%d %n %H:%M:%S")
                except:
                    print('New problem , must standarize the time')
                    pass



        else:
            date = post.published
            try:
                a=datetime.strptime(date,"%Y-%m-%d %n %H:%M:%S")
                print('jawha behi')
            except:
                a=date
                a = a[0:10] + ' ' + a[11:19] + ' ' + a[19:22] + a[23:]
                try:
                    date = datetime.strptime(a, "%Y-%m-%d %H:%M:%S %z")
                    c = date - date.utcoffset()
                    date=c.strftime("%Y-%m-%d %n %H:%M:%S")
                except:
                    print('new prob')



        rss_dict.update(
                {post.link:
                {'base_url': d.feed.link,
                'headline': post.title,
                'article_link': post.link,
                'author': post.get('author','Author not found'),
                'published_date':date,
                'article_text': article_text,
                 'summary':summary
            }})




d = list(rss_dict.values())

for post in d:
    cur.execute("insert into news_list (base_url,headline,article_link,author,published_date,article_text,summary) values (%s,%s,%s,%s,%s,%s,%s)",(post.get('base_url'),post.get('headline'),post.get('article_link'),post.get('author'),post.get('published_date'),post.get('article_text'),post.get('summary')))
    con.commit()
    count+=1



with open("/home/dan/scraping_results.txt", "a") as file_object:

    # Append 'hello' at the end of file
    file_object.write("\n")
    file_object.write(f"Added {count} articles in about {datetime.now() - startTime}")


con.close()



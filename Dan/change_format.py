import psycopg2
from datetime import datetime

from gensim.summarization import summarize

# connect to db

con = psycopg2.connect(
    host='localhost',
    database="news",
    user='postgres',
    password='admin',
)
# cursor
cur = con.cursor()
cur.execute(f"SELECT id,article_text from news_list limit 35000")
rows = cur.fetchall()
print(len(rows))

current_links_list = [r for r in rows]
for r in current_links_list:
    sql_update_query = """Update news_list set summary = %s where id = %s"""
    article_text = r[1]
    summary=''
    try:
        summary = summarize(article_text, ratio=0.04, word_count=100)
    except :

        try:
            summary = summarize(article_text, word_count=100)
        except:
            n = article_text.find('.')
            try:
                summary = summarize(article_text[n + 1:])
            except Exception as e:
                print(f"{e} and the article text={article_text[:10]}")


    if summary=='':
        summary=article_text
    cur.execute(sql_update_query, (summary, r[0]))
    con.commit()

# print(current_links_list)
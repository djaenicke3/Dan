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
cur.execute(f"SELECT id,article_text from news_list where summary ='' limit 10 ")
rows = cur.fetchall()
print(len(rows))
print()
print(rows[1][1])
current_links_list = [r for r in rows]
for r in current_links_list:
    sql_update_query = """Update news_list set summary = %s where id = %s"""
    article_text = r[1]
    try:
        summary_text = summarize(article_text, ratio=0.04, word_count=100)
    except Exception as e:
        print(e)
        summary_text='Cannot summarize article , Click on article link'
    if summary_text== '':
        summary_text='Cannot summarize article , Click on article link'
    cur.execute(sql_update_query, (summary_text, r[0]))
    con.commit()

# print(current_links_list)
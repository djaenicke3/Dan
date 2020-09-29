import psycopg2
from datetime import datetime


def convert(date):
    if 'T' not in date:
        return date
    a = date
    a = a[0:10] + ' ' + a[11:19] + ' ' + a[19:22] + a[23:]
    try:
        date = datetime.strptime(a, "%Y-%m-%d %H:%M:%S %z")
        c = date - date.utcoffset()
        date = c.strftime("%Y-%m-%d %n %H:%M:%S")
    except Exception as e:
        print(e)
    return date


# connect to db

con = psycopg2.connect(
    host='localhost',
    database="news",
    user='postgres',
    password='admin',
)
# cursor
cur = con.cursor()
link = 'https://www.theatlantic.com/'
cur.execute(f"SELECT id,published_date FROM news_list where base_url='{link}' and  published_date ~ 'T' ")
rows = cur.fetchall()
current_links_list = [r for r in rows]
print(current_links_list)
for r in current_links_list:
    sql_update_query = """Update news_list set published_date = %s where id = %s"""
    cur.execute(sql_update_query, (convert(r[1]), r[0]))
    con.commit()

# print(current_links_list)
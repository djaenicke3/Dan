import psycopg2

#connect to db

con=psycopg2.connect(
    host='localhost',
    database="news",
    user='postgres',
    password='admin',
)
cur=con.cursor()

cur.execute("SELECT id, summary from news_list limit 5")

rows = cur.fetchall()

for row in rows:
    sql_update_query = """Update news_list set summary = %s where id = %s"""
    if row[1]:
        shorten = row[1][:50]
        cur.execute(sql_update_query, (row[0], shorten))
        print(shorten)
    else:
        pass
    
    
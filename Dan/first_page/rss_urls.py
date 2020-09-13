from .models import NewsList
from django.db import connection


urls=['']
cursor = connection.cursor()
cursor.execute("SELECT DISTINCT base_url FROM news_list")
for url in cursor.fetchall():
	urls.append(url[0])





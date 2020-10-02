# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class NewsList(models.Model):
    id = models.IntegerField(primary_key=True)
    base_url = models.TextField(blank=True, null=True)
    headline = models.TextField(blank=True, null=True)
    article_link = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    published_date = models.TextField(blank=True, null=True)
    article_text = models.TextField(blank=True, null=True)
    summary=models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'news_list'

    def __str__(self):
        return self.headline
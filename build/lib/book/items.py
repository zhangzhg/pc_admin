# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from backend.models import BookItem
from backend.models import BookChapter


class BookItem(DjangoItem):
    django_model = BookItem


class BookChapter(DjangoItem):
    django_model = BookChapter

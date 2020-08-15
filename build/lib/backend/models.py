from django.db import models


# 檢索數據目錄表
class BookIndex(models.Model):
    # 書名
    title = models.CharField(max_length=100)
    # 描述
    desc = models.CharField(max_length=100)
    # 作者
    author = models.CharField(max_length=10)
    # 最新更新时间
    lastUpdateTime = models.CharField(max_length=10)
    # 最新章节
    lastChapter = models.CharField(max_length=100)
    # 已读章节
    durChapter = models.CharField(max_length=100)
    # 已读章节
    url = models.CharField(max_length=100)


# 每个章节详情
class BookItem(models.Model):
    # 章节名
    title = models.CharField(max_length=100)
    # 当前页
    url = models.CharField(max_length=200)
    # 内容
    content = models.CharField(max_length=20000)


class BookChapter(models.Model):
    # 章节名
    title = models.CharField(max_length=100)
    # 当前页
    count = models.IntegerField()
    # 链接地址
    url = models.CharField(max_length=100)
    # 书名
    name = models.CharField(max_length=100)
    # 是否已加载
    load = models.IntegerField()
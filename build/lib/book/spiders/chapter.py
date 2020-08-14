# -*- coding: UTF-8 -*-
from book.items import BookChapter
import scrapy

# 启动命令：scrapy crawl chapter
class ChapterSpider(scrapy.Spider):  # 需要继承scrapy.Spider类
    name = "chapter"  # 定义蜘蛛名


    def __init__(self, u=None, **kwargs):
        self.urls = [u]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):
        # 保存数据
        alla = response.xpath('//div[@id="list"]/dl/dd')
        name = response.xpath('//div[@id="info"]/h1/text()').get()
        c = 1
        for a in alla:
            item = BookChapter()
            text = a.xpath('.//a/text()').get()
            href = a.xpath('.//a/@href').get()
            item['name'] = name
            item['title'] = text
            item['url'] = href
            item['count'] = c
            item['load'] = 0
            c += 1
            yield item

# -*- coding: UTF-8 -*-
from book.items import BookItem
import logging
import scrapy
import time


# from environment import Environment

# 启动命令：scrapy crawl biqu
class BiquSpider(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "biqu"  # 定义蜘蛛名

    # def start_requests(self): # 由此方法通过下面链接爬取页面

    # 定义爬取的链接
    # urls = [
    #     'http://www.biquge.info/90_90350/19785047.html'
    # ]

    # scrapy shell http://www.biquge.info/22_22533/8100293.html
    # start_urls = ['http://www.biquge.info/90_90350/19785047.html']
    def __init__(self, u=None, n=0, **kwargs):
        self.urls = [u]
        self.next = int(n)

    # def __init__(self):
    #     self.urls = ['http://www.xbiquge.la/0/75/61207.html']
    #     self.next = 1

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, meta={"url": url, "next": self.next}, callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):

        '''
        start_requests已经爬取到页面，那如何提取我们想要的内容呢？那就可以在这个方法里面定义。
        这里的话，并木有定义，只是简单的把页面做了一个保存，并没有涉及提取我们想要的数据，后面会慢慢说到
        也就是用xpath、正则、或是css进行相应提取，这个例子就是让你看看scrapy运行的流程：
        1、定义链接；
        2、通过链接爬取（下载）页面；
        3、定义规则，然后提取数据；
        就是这么个流程，似不似很简单呀？
        '''
        meta = response.meta

        filename = response.xpath('//div[@class="bookname"]/h1/text()').extract_first()
        if filename is not None:
            filename = filename.replace("正文", "").strip()
        else:
            return

        if 'next' in meta:
            next = meta['next']
        else:
            next = 0
        if 'url' in meta:
            url = meta['url']
        else:
            url = ''
        # 保存数据
        item = BookItem()
        item['url'] = url
        item['title'] = filename
        contents = response.xpath('//div[@id="content"]/text()').extract()
        content = ''
        for it in contents:
            if it == '\r\n':
                continue
            content += it + '\r\n'
        item['content'] = content
        yield item

        # 不自动查找下一页， 直接停止
        if next == 0:
            return

        taga = response.xpath('//div[@class="bottem1"]/a')  # css选择器提取下一页链接

        next_page = ''
        for a in taga:
            ts = a.xpath('text()').extract_first()
            if ts == '下一章':
                next_page = a.xpath('@href').extract_first()
                break
        logging.info(next_page)
        if next_page.strip() != '':  # 判断是否存在下一页
            next_page = response.urljoin(next_page)
            # 太快网站会返回失败信息
            yield scrapy.Request(next_page, meta={"url": next_page, "next": 1}, callback=self.parse)

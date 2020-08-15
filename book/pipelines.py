# -*- coding: utf-8 -*-
import pymysql
import unicodedata
from book.items import *
import logging
from pc_admin.settings import ROOT_URL
# from scrapy.utils.project import get_project_settings

class BookPipeline(object):
    def __init__(self):
        # settings = get_project_settings()
        host = '127.0.0.1'
        user = 'root'
        psd = 'root'
        db = 'book'
        self.conn = pymysql.connect(host, user, psd, db)
        self.c = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            exists_sql = "select 1 from backend_bookitem where url=%s limit 1"
            self.c.execute(exists_sql, (item['url']))
            res = self.c.fetchone()
            content = self.filter_word(item['content'])
            if res and len(res) > 0:
                sql = "update backend_bookitem set content=%s where title=%s".format(content, item['url'])
                self.c.execute(sql, (content, item['url']))
            else:
                sql = "insert into backend_bookitem(title,url,content) values (%s,%s,%s)"
                self.c.execute(sql, (item['title'], item['url'], content))

            sql = "update backend_bookchapter set `load`=1 where url=%s"
            self.c.execute(sql, (item['url'].replace(ROOT_URL, '')))

            self.conn.commit()
            return item

        elif isinstance(item, BookChapter):
            exists_sql = "select max(count) from backend_bookchapter where name=%s"
            self.c.execute(exists_sql, (item['name']))
            res = self.c.fetchone()

            if len(res) > 0 and res[0] is not None and res[0] >= item['count']:
                logging.info('>>>>>>>>>>>>>exists<<<<<<<<<<<<<<')
                return item
            # sql = "insert into backend_bookchapter(title,name,count,url,`load`) values (%s, %s, %s, %s, s%)"
            # self.c.execute(sql, (item['title'], item['name'], item['count'], item['url'], 0))
            sql = "insert into backend_bookchapter(title,name,count,url,`load`) values ('{}','{}','{}', '{}', '{}')".format(
                item['title'], item['name'], item['count'], item['url'], 0)
            logging.info(sql)
            self.c.execute(sql)
            self.conn.commit()
            return item

    def spider_close(self, spider):
        self.c.close()
        self.conn.close()

    # 转义字符去掉
    def filter_word(self, content):
        content = unicodedata.normalize('NFKC', content)
        content = content.replace("/", "");
        content = content.replace("'", "");
        content = content.replace("[", "");
        content = content.replace("]", "");
        content = content.replace("%", "");
        content = content.replace("&", "");
        content = content.replace("_", "");
        content = content.replace("(", "");
        content = content.replace(")", "");
        return content;

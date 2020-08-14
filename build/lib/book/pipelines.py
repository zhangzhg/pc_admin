# -*- coding: utf-8 -*-
import sqlite3
import unicodedata
from book.items import *
import logging
from book.settings import DB_PATH
from pc_admin.settings import ROOT_URL

class BookPipeline(object):
    def open_spider(self, spider):
        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            exists_sql = "select 1 from backend_bookitem where url='{}' limit 1".format(item['url'])
            self.c.execute(exists_sql)
            res = self.c.fetchone()
            content = self.filter_word(item['content'])
            if res and len(res) > 0:
                sql = "update backend_bookitem set content='{}' where title='{}'".format(content, item['url'])
            else:
                sql = "insert into backend_bookitem('title','url','content') values ('{}','{}', '{}')".format(
                    item['title'], item['url'], content)
            self.c.execute(sql)

            sql = "update backend_bookchapter set load=1 where url='{}'".format(item['url'].replace(ROOT_URL, ''))
            self.c.execute(sql)

            self.conn.commit()
            return item

        elif isinstance(item, BookChapter):
            exists_sql = "select max(count) from backend_bookchapter where name='{}'".format(item['name'])
            self.c.execute(exists_sql)
            res = self.c.fetchone()

            if len(res) > 0 and res[0] is not None and res[0] >= item['count']:
                logging.info('>>>>>>>>>>>>>exists<<<<<<<<<<<<<<')
                return item
            sql = "insert into backend_bookchapter('title','name','count','url') values ('{}','{}','{}', '{}')".format(
                item['title'], item['name'], item['count'], item['url'])
            self.c.execute(sql)
            self.conn.commit()
            return item

    def spider_close(self, spider):
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

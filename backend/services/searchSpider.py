from ..models import BookIndex

class SearchSpider:
    def __init__(self, response):
        self.response = response

    def doList(self):
        list = []
        trs = self.response.xpath('//*[@id="checkform"]/table/tr')
        for tr in trs:
            tds = tr.xpath('.//td//text()').extract()
            if len(tds) == 0:
                continue
            item = BookIndex()
            offset = 0
            for i in range(len(tds)):
                value = tds[i].replace(" ", "")
                value = value.strip('\n')
                value = value.strip('\n')
                if value == '':
                    offset += 1
                    continue
                if i == 0:
                    href = tr.xpath('.//td/a/@href').extract_first()
                    item.url = href
                    item.title = value
                elif i == offset+1:
                    item.lastChapter = value
                elif i == offset+2:
                    item.author = value
                elif i == offset+3:
                    item.lastUpdateTime = value
            list.append(item)
        return list

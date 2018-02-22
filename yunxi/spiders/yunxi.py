import scrapy
import time
from scrapy.http import Request, FormRequest
import json

class YunSee(scrapy.Spider):
    def _init_(self,search_host = None):
        if search_host is None:
             print '-a search_host =url'
        else:
             self.search_host=search_host
    name = 'yunxi'
   # search_host = None

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Host':'www.yunsee.cn',
        'Referer':'http://www.yunsee.cn/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }

    def start_requests(self):
        url = 'http://www.yunsee.cn/geetest?t=%s' % (int(time.time()) * 1000)
        yield Request(url=url, headers=self.headers, callback=self.parse_token)

    def parse_token(self, response):
        result = json.loads(response.body)
        gt = result['gt']
        challenge = result['challenge']
        url = 'http://www.yunsee.cn/finger.html'
        yield Request(url=url, headers=self.headers, meta={'gt':gt, 'challenge':challenge}, callback=self.parse_index_token)

    def parse_index_token(self, response):
        token = response.xpath('//meta[@name="csrf-token"]/@content').extract()
        if token and len(token) > 0:
            token=token[0]
            self.headers.update({'X-CSRF-TOKEN': token})
            url = 'http://www.yunsee.cn/finger.html'
            form = {
                'string': self.search_host,
                'http': '2',
                'level': '2',
                'code': 'd879af'+str((len(self.search_host)-1)*(len(self.search_host)+1)*3)+'g54df45',
            }
            yield FormRequest(url=url, formdata=form, headers=self.headers, callback=self.parse)
        else:
            yield "error"

    def parse(self, response):
        print response.body


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    import os
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'yunxi.settings'
    process = CrawlerProcess()
    #search_host = sys.argv[1]
    #process.crawl(YunSee,search_host='www.baidu.com')
    process.crawl(YunSee,search_host)
    process.start()

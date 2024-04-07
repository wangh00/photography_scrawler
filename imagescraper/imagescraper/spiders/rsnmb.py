import scrapy
from scrapy.utils.project import get_project_settings
from scrapy import signals


class RsnmbSpider(scrapy.Spider):
    name = "rsnmb"
    allowed_domains = ["www.rsnmb.com"]
    # # start_urls = ["http://www.rsnmb.com/"]
    #
    # def __init__(self, start_url='http://www.rsnmb.com/', *args, **kwargs):
    #     super(RsnmbSpider, self).__init__(*args, **kwargs)
    #     self.start_urls = [start_url]
    default_start_url = 'https://www.rsnmb.com/'
    crawl_page_count = None  # 指定要爬取的页数
    counts = 0

    def __init__(self, start_url=None,page_count=None, *args, **kwargs):
        super(RsnmbSpider, self).__init__(*args, **kwargs)
        if page_count:
            self.crawl_page_count=int(page_count)
        if start_url:
            self.start_urls = [start_url]
        else:
            self.start_urls = [self.default_start_url]


    def parse(self, response):
        # 解析出合集的链接
        collections = response.xpath('//div[@class="post-lists-body"]/div[@class="post-onelist-item"]')
        for collection_url in collections:
            url_one = collection_url.xpath('.//div[@class="item-title"]/a/@href').get(default='')
            title_one = collection_url.xpath('.//div[@class="item-title"]/a/text()').get(default='')
            print(url_one,title_one)
            yield scrapy.Request(url_one, callback=self.parse_collection,meta={'title':title_one})
        # 翻页处理，生成下一页的请求
        self.counts += 1
        if self.crawl_page_count and self.counts >= self.crawl_page_count:
            print('已采集到需求数量，终止')
            self.crawler.signals.send_catch_log(signal=signals.spider_closed, spider=self,reason='crawl_page_count_reached')
        else:
            next_page = response.xpath('//li[@class="next"]/a/@href').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)

    def parse_collection(self, response):
        title = response.meta['title'].replace(':','-')
        # 解析合集页面中的图片链接
        image_urls = response.xpath('//div[@id="post-content"]//img/@src').getall()
        for index,image_url in enumerate(image_urls):
            image_name=f'{self.name}/{title}/{index+1}.jpg'
            # print(image_url)
            yield {
                'image_urls': [image_url],
                'image_name': image_name  # 或任何有助于构建文件名的信息
            }

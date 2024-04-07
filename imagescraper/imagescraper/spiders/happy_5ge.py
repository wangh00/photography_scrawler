import scrapy


class Happy5geSpider(scrapy.Spider):
    name = "happy_5ge"
    allowed_domains = ["happy.5ge.net"]
    default_start_url = "https://happy.5ge.net/category/图册"


    def __init__(self, start_url=None, *args, **kwargs):
        super(Happy5geSpider, self).__init__(*args, **kwargs)
        if start_url:
            self.start_urls = [start_url]
        else:
            self.start_urls = [self.default_start_url]


    def parse(self, response):
        # 解析出合集的链接
        collections = response.xpath('//div[@class="joe_archive"]//li[contains(@class,"joe_list__item")]')
        for collection_url in collections:
            url_one = collection_url.xpath('./a[@title]/@href').get(default='')
            title_one = collection_url.xpath('./a[@title]/@title').get(default='')
            print(url_one,title_one)
            yield scrapy.Request(url_one, callback=self.parse_collection,meta={'title':title_one})
        # 翻页处理，生成下一页的请求
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_collection(self, response):
        title = response.meta['title'].replace(':','-')
        # 解析合集页面中的图片链接
        image_urls = response.xpath('//article[@class="joe_detail__article"]//img/@data-src').getall()
        for index,image_url in enumerate(image_urls):
            image_name=f'{self.name}/{title}/{index+1}.jpg'
            image_url=image_url.replace('https://static.5ge.net/image','https://i0.wp.com/static.2ge.org/tg')
            print(image_url,image_name)
            yield {
                'image_urls': [image_url],
                'image_name': image_name  # 或任何有助于构建文件名的信息
            }

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ImagescraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ImagescraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # request.meta['proxy'] = self.get_proxy()
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        print(f'-{spider.name}--error--{request.url}--{exception}')  # 这个地址没有爬
        pass

    def get_proxy(self):
        import requests
        res = requests.get('http://127.0.0.1:5010/get/').json()
        if res.get('https'):
            return 'https://' + res.get('proxy')
        else:
            return 'http://' + res.get('proxy')


    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class CustomHeadersMiddleware:
    def __init__(self, headers):
        self.headers = headers

    @classmethod
    def from_crawler(cls, crawler):
        # 从 settings.py 中获取全局的默认请求头
        headers = crawler.settings.getdict('DEFAULT_REQUEST_HEADERS', {})
        return cls(headers)

    def process_request(self, request, spider):
        # 根据不同的爬虫设置不同的请求头
        if spider.name == 'happy_5ge':
            custom_headers = {'User-Agent': 'UserAgent1'}
        elif spider.name == 'rsnmb':
            custom_headers = {'User-Agent': 'UserAgent1'}
        else:
            custom_headers = {}

        # 合并默认请求头和自定义请求头
        final_headers = {**self.headers, **custom_headers}

        # 将最终的请求头设置到 Request 对象中
        request.headers.update(final_headers)
        return None
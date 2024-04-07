# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

from imagescraper.spiders.happy_5ge import Happy5geSpider
from imagescraper.spiders.rsnmb import RsnmbSpider

def main1():
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(Happy5geSpider)
    runner.crawl(RsnmbSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


def main2():
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    # running spiders sequentially (non-distributed)
    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(Happy5geSpider)
        yield runner.crawl(RsnmbSpider)
        reactor.stop()
    crawl()
    reactor.run()
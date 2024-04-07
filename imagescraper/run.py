# -*- coding: utf-8 -*-

from scrapy import cmdline, Spider



if __name__ == '__main__':
    cmdline.execute("scrapy crawl rsnmb -a start_url=https://www.rsnmb.com/index.php/page/461/ -a page_count=1".split())


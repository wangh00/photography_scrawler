# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy




class ImagescraperItem(scrapy.Item):
    image_urls = scrapy.Field()
    image_name = scrapy.Field()  # 用于存储文件名或相关信息
